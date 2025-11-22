# game_engine.py

from dataclasses import dataclass, field
from typing import Dict, List
import datetime
import os
import requests

# Ativos permitidos no jogo (pode ser estático no MVP)
ASSETS = {
    "PETR4": 37.50,
    "ITUB4": 29.10,
    "VALE3": 62.30,
    "BOVA11": 110.40,
    "MGLU3": 2.45,
}

DEFAULT_INITIAL_CASH = 10000.0


ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"

# Mapeia tickers do jogo para o símbolo na API (B3 costuma usar .SA)
ALPHA_SYMBOLS = {
    "PETR4": "PETR4.SA",
    "ITUB4": "ITUB4.SA",
    "VALE3": "VALE3.SA",
    "BOVA11": "BOVA11.SA",
    "MGLU3": "MGLU3.SA",
}


def get_live_price(ticker: str) -> float:
    """
    Busca o preço ao vivo na Alpha Vantage.
    Se der erro ou não tiver API key, retorna 0.0
    (o Tournament depois faz fallback pro ASSETS).
    """
    if not ALPHA_VANTAGE_API_KEY:
        print("ALPHA_VANTAGE_API_KEY não configurada, usando preço estático.")
        return 0.0

    symbol = ALPHA_SYMBOLS.get(ticker.upper())
    if not symbol:
        print(f"Ticker {ticker} não mapeado para Alpha Vantage.")
        return 0.0

    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY,
    }

    try:
        resp = requests.get(ALPHA_VANTAGE_URL, params=params, timeout=10)
        data = resp.json()
        quote = data.get("Global Quote") or data.get("Global_Quote")
        if not quote:
            print("Resposta da API sem 'Global Quote':", data)
            return 0.0

        price_str = quote.get("05. price")
        if not price_str:
            print("Campo '05. price' não encontrado na resposta:", quote)
            return 0.0

        return float(price_str)
    except Exception as e:
        print("Erro ao buscar preço ao vivo:", e)
        return 0.0



@dataclass
class Position:
    ticker: str
    quantity: int
    avg_price: float  # preço médio


@dataclass
class Player:
    phone: str  # id do jogador (número do WhatsApp)
    name: str = ""
    cash: float = 0.0  # vai ser definido pelo torneio
    positions: Dict[str, "Position"] = field(default_factory=dict)


    def total_equity(self) -> float:
        portfolio_value = 0.0
        for pos in self.positions.values():
            current_price = get_live_price(pos.ticker) or ASSETS.get(pos.ticker, 0.0)
            portfolio_value += pos.quantity * current_price
        return self.cash + portfolio_value


    def diversification_score(self) -> float:
        """
        Score simples de diversificação:
        só conta quantos ativos diferentes o cara tem.
        Pode sofisticar depois (índice de concentração etc).
        """
        return len(self.positions)


@dataclass
class Trade:
    player_phone: str
    ticker: str
    quantity: int
    price: float
    side: str  # "BUY" ou "SELL"
    timestamp: datetime.datetime


class Tournament:
    def __init__(
        self,
        name: str,
        days_duration: int = 7,
        initial_cash: float = DEFAULT_INITIAL_CASH,
        max_players: int | None = None,
    ):
        self.name = name
        self.start_date = datetime.datetime.now()
        self.end_date = self.start_date + datetime.timedelta(days=days_duration)
        self.initial_cash = initial_cash
        self.max_players = max_players
        self.days_duration = days_duration

        self.players: Dict[str, Player] = {}
        self.trades: List[Trade] = []

    def configure(
        self,
        max_players: int | None = None,
        days_duration: int | None = None,
        initial_cash: float | None = None,
    ):
        """Permite reconfigurar o torneio (ex: no início do jogo)."""
        if max_players is not None:
            self.max_players = max_players

        if days_duration is not None:
            self.days_duration = days_duration
            self.start_date = datetime.datetime.now()
            self.end_date = self.start_date + datetime.timedelta(days=days_duration)

        if initial_cash is not None:
            self.initial_cash = initial_cash

        # opcional: resetar jogadores/posições se você quiser um torneio novo
        # self.players.clear()
        # self.trades.clear()

    # ---------- Jogadores --------------

    def join_player(self, phone: str, name: str = "") -> Player:
        # Se já está no torneio, só atualiza o nome (se vier) e retorna
        if phone in self.players:
            player = self.players[phone]
            if name:
                player.name = name
            return player

        # Checa limite de players
        if self.max_players is not None and len(self.players) >= self.max_players:
            raise ValueError(
                f"Limite de {self.max_players} jogadores já foi atingido."
            )

        # Cria jogador com saldo inicial definido no torneio
        player = Player(phone=phone, name=name, cash=self.initial_cash)
        self.players[phone] = player
        return player


    def get_player(self, phone: str) -> Player | None:
        return self.players.get(phone)

    # ---------- Preços (MVP) --------------
    def get_price(self, ticker: str) -> float:
        ticker = ticker.upper()
        live_price = get_live_price(ticker)
        if live_price > 0:
            return live_price

        fallback = ASSETS.get(ticker, 0.0)
        print(f"[FALLBACK] Usando preço estático de {ticker} = {fallback}")
        return fallback



    # ---------- Operações --------------

    def buy(self, phone: str, ticker: str, quantity: int) -> str:
        ticker = ticker.upper()
        if ticker not in ASSETS:
            return f"Ativo {ticker} não é permitido neste torneio."

        if quantity <= 0:
            return "Quantidade deve ser positiva."

        player = self.join_player(phone)
        price = self.get_price(ticker)
        cost = price * quantity

        if cost > player.cash:
            return (
                f"Saldo insuficiente. Compra custaria R$ {cost:.2f}, "
                f"mas você só tem R$ {player.cash:.2f}."
            )

        # Atualiza caixa
        player.cash -= cost

        # Atualiza posição
        if ticker not in player.positions:
            player.positions[ticker] = Position(
                ticker=ticker, quantity=quantity, avg_price=price
            )
        else:
            pos = player.positions[ticker]
            new_quantity = pos.quantity + quantity
            new_avg_price = (
                pos.quantity * pos.avg_price + quantity * price
            ) / new_quantity
            pos.quantity = new_quantity
            pos.avg_price = new_avg_price

        # Registra trade
        self.trades.append(
            Trade(
                player_phone=phone,
                ticker=ticker,
                quantity=quantity,
                price=price,
                side="BUY",
                timestamp=datetime.datetime.now(),
            )
        )
        

        return (
            f"✅ Compra realizada: {quantity}x {ticker} a R$ {price:.2f} (preço ao vivo).\n"
            f"Saldo atual: R$ {player.cash:.2f}."
        )


    def sell(self, phone: str, ticker: str, quantity: int) -> str:
        ticker = ticker.upper()
        player = self.get_player(phone)
        if not player:
            return "Você ainda não entrou no torneio. Envie 'entrar' primeiro."

        if ticker not in player.positions:
            return f"Você não possui o ativo {ticker} na carteira."

        if quantity <= 0:
            return "Quantidade deve ser positiva."

        pos = player.positions[ticker]
        if quantity > pos.quantity:
            return f"Você não tem essa quantidade. Tem {pos.quantity}x {ticker} na carteira."

        price = self.get_price(ticker)
        proceeds = price * quantity

        # Atualiza posição
        pos.quantity -= quantity
        if pos.quantity == 0:
            del player.positions[ticker]

        # Atualiza caixa
        player.cash += proceeds

        # Registra trade
        self.trades.append(
            Trade(
                player_phone=phone,
                ticker=ticker,
                quantity=quantity,
                price=price,
                side="SELL",
                timestamp=datetime.datetime.now(),
            )
        )

        return (
            f"✅ Venda realizada: {quantity}x {ticker} a R$ {price:.2f}.\n"
            f"Saldo atual: R$ {player.cash:.2f}."
        )

    # ---------- Relatórios --------------

    def portfolio_summary(self, phone: str) -> str:
        player = self.get_player(phone)
        if not player:
            return "Você ainda não entrou no torneio. Envie 'entrar' para começar."

        lines = []
        lines.append(f"📊 Carteira de {player.name or phone}:")
        lines.append(f"- Saldo em caixa: R$ {player.cash:.2f}")
        lines.append("")

        if not player.positions:
            lines.append("Você ainda não possui ativos.")
        else:
            lines.append("Posições:")
            for pos in player.positions.values():
                current_price = self.get_price(pos.ticker)
                total_value = current_price * pos.quantity
                lines.append(
                    f"• {pos.ticker}: {pos.quantity}x "
                    f"(PM R$ {pos.avg_price:.2f}) "
                    f"| Preço atual R$ {current_price:.2f} "
                    f"| Total R$ {total_value:.2f}"
                )

        lines.append("")
        lines.append(f"Valor total da carteira: R$ {player.total_equity():.2f}")
        lines.append(
            f"Ativos diferentes (diversificação): {player.diversification_score()}"
        )

        # Mensagem educativa simples
        if player.diversification_score() <= 1:
            lines.append(
                "⚠ Sua carteira está pouco diversificada. Considere incluir mais ativos."
            )
        else:
            lines.append("✅ Boa! Você já está diversificando entre mais de um ativo.")

        return "\n".join(lines)

    def ranking(self) -> str:
        if not self.players:
            return "Ninguém entrou no torneio ainda."

        players_sorted = sorted(
            self.players.values(),
            key=lambda p: p.total_equity(),
            reverse=True,
        )

        lines = []
        lines.append("🏆 Ranking por patrimônio total:")
        for i, p in enumerate(players_sorted, start=1):
            lines.append(f"{i}. {p.name or p.phone}: R$ {p.total_equity():.2f}")

        # Ranking de diversificação
        players_div_sorted = sorted(
            self.players.values(),
            key=lambda p: p.diversification_score(),
            reverse=True,
        )

        lines.append("")
        lines.append("📈 Ranking por diversificação (mais ativos diferentes):")
        for i, p in enumerate(players_div_sorted, start=1):
            lines.append(
                f"{i}. {p.name or p.phone}: {p.diversification_score()} ativos"
            )

        return "\n".join(lines)


