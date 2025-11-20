# game_engine.py

from dataclasses import dataclass, field
from typing import Dict, List
import datetime

# Ativos permitidos no jogo (pode ser estático no MVP)
ASSETS = {
    "PETR4": 37.50,
    "ITUB4": 29.10,
    "VALE3": 62.30,
    "BOVA11": 110.40,
    "MGLU3": 2.45,
}

INITIAL_CASH = 10000.0


@dataclass
class Position:
    ticker: str
    quantity: int
    avg_price: float  # preço médio


@dataclass
class Player:
    phone: str  # id do jogador (número do WhatsApp)
    name: str = ""
    cash: float = INITIAL_CASH
    positions: Dict[str, Position] = field(default_factory=dict)

    def total_equity(self) -> float:
        """Valor total da carteira (caixa + posição em ações)."""
        portfolio_value = 0.0
        for pos in self.positions.values():
            current_price = ASSETS.get(pos.ticker, 0.0)
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
    def __init__(self, name: str, days_duration: int = 7):
        self.name = name
        self.start_date = datetime.datetime.now()
        self.end_date = self.start_date + datetime.timedelta(days=days_duration)
        self.players: Dict[str, Player] = {}
        self.trades: List[Trade] = []

    # ---------- Jogadores --------------

    def join_player(self, phone: str, name: str = "") -> Player:
        if phone not in self.players:
            self.players[phone] = Player(phone=phone, name=name)
        return self.players[phone]

    def get_player(self, phone: str) -> Player | None:
        return self.players.get(phone)

    # ---------- Preços (MVP) --------------

    def get_price(self, ticker: str) -> float:
        """No MVP, usa o preço fixo de ASSETS."""
        return ASSETS.get(ticker.upper(), 0.0)

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
            f"✅ Compra realizada: {quantity}x {ticker} a R$ {price:.2f}.\n"
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
    
    # app.py

