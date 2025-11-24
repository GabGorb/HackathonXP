from dataclasses import dataclass, field, asdict
from typing import Dict, List
import datetime
import os
import requests
import database
import heapq

# --- CONFIGURAÇÕES E DADOS DE MERCADO ---

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
    Se der erro ou não tiver API key, retorna o valor estático de ASSETS.
    """
    if not ALPHA_VANTAGE_API_KEY:
        return ASSETS.get(ticker, 0.0)

    symbol = ALPHA_SYMBOLS.get(ticker)
    if not symbol:
        return ASSETS.get(ticker, 0.0)

    try:
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": ALPHA_VANTAGE_API_KEY
        }
        response = requests.get(ALPHA_VANTAGE_URL, params=params, timeout=5)
        data = response.json()
        
        # Parse da resposta da Alpha Vantage
        quote = data.get("Global Quote", {})
        price_str = quote.get("05. price")
        
        if price_str:
            return float(price_str)
        else:
            return ASSETS.get(ticker, 0.0)
            
    except Exception as e:
        print(f"Erro na API de finanças: {e}")
        return ASSETS.get(ticker, 0.0)


# --- CLASSES DO JOGO ---

@dataclass
class Player:
    phone: str
    name: str
    cash: float
    portfolio: Dict[str, int] = field(default_factory=dict)

    def total_equity(self) -> float:
        """Calcula Saldo + Valor das Ações (marcadas a mercado)"""
        equity = self.cash
        for ticker, qty in self.portfolio.items():
            price = get_live_price(ticker)
            equity += price * qty
        return equity

    def diversification_score(self) -> int:
        """Retorna quantos ativos diferentes o jogador tem (educativo)"""
        return len(self.portfolio)

    @staticmethod
    def from_dict(data: dict):
        """Reconstrói o objeto Player a partir dos dados do Firebase"""
        if not data:
            return None
        return Player(
            phone=data.get("phone"),
            name=data.get("name"),
            cash=float(data.get("cash", 0.0)),
            portfolio=data.get("portfolio", {})
        )


class Tournament:
    def __init__(self, name: str, days_duration: int, initial_cash: float, max_players: int = None):
        self.name = name
        self.days_duration = days_duration
        self.initial_cash = initial_cash
        self.max_players = max_players
   
    def _get_player(self, phone: str) -> Player:
        """Busca jogador no banco e retorna objeto Player."""
        data = database.get_player_data(phone)
        if data:
            return Player.from_dict(data)
        return None

    def _save_player(self, player: Player):
        """Salva o estado atual do jogador no banco."""
        data = asdict(player)
        database.save_player_data(player.phone, data)

    def add_player(self, phone: str, name: str = None) -> Player:
        """Registra um novo jogador se ele não existir."""
        existing = self._get_player(phone)
        if existing:
            return existing

        new_player = Player(
            phone=phone,
            name=name,
            cash=self.initial_cash,
            portfolio={}
        )
        
        self._save_player(new_player)
        print(f"Novo jogador salvo: {name} ({phone})")
        return new_player

    def buy(self, phone: str, ticker: str, qty: int) -> str:
        """Processa compra de ativos."""
        if ticker not in ASSETS:
            return f"Ativo inválido. Disponíveis: {list(ASSETS.keys())}"
        
        if qty <= 0:
            return "A quantidade deve ser positiva."

        player = self._get_player(phone)
        if not player:
            return "Você ainda não entrou no torneio. Use 'entrar SEU_NOME'."

        price = get_live_price(ticker)
        cost = price * qty

        if player.cash < cost:
            return f"Saldo insuficiente! Custo: R$ {cost:.2f} | Seu Saldo: R$ {player.cash:.2f}"

        player.cash -= cost
        player.portfolio[ticker] = player.portfolio.get(ticker, 0) + qty

        self._save_player(player)

        return (
            f"✅ Compra realizada!\n"
            f"Ativo: {ticker}\n"
            f"Qtd: {qty}\n"
            f"Preço un: R$ {price:.2f}\n"
            f"Saldo restante: R$ {player.cash:.2f}"
        )

    def sell(self, phone: str, ticker: str, qty: int) -> str:
        """Processa venda de ativos."""
        if ticker not in ASSETS:
            return "Ativo inválido."
        
        if qty <= 0:
            return "Quantidade inválida."

        player = self._get_player(phone)
        if not player:
            return "Você não está no jogo."

        current_qty = player.portfolio.get(ticker, 0)
        if current_qty < qty:
            return f"Você só tem {current_qty} ações de {ticker}."

        price = get_live_price(ticker)
        total_sale = price * qty

        player.cash += total_sale
        player.portfolio[ticker] = current_qty - qty
        
        if player.portfolio[ticker] == 0:
            del player.portfolio[ticker]

        self._save_player(player)

        return (
            f"💰 Venda realizada!\n"
            f"Ativo: {ticker}\n"
            f"Valor recebido: R$ {total_sale:.2f}\n"
            f"Saldo atual: R$ {player.cash:.2f}"
        )

    def portfolio_summary(self, phone: str) -> str:
        """Retorna resumo da carteira do jogador."""
        player = self._get_player(phone)
        if not player:
            return "Você não está no jogo. Digite 'entrar SEU_NOME'."

        lines = [f"👤 Carteira de {player.name or phone}:"]
        lines.append(f"💵 Saldo em conta: R$ {player.cash:.2f}")
        
        total_invested = 0.0
        if player.portfolio:
            lines.append("--- Ações ---")
            for ticker, qty in player.portfolio.items():
                curr_price = get_live_price(ticker)
                val = curr_price * qty
                total_invested += val
                lines.append(f"{ticker}: {qty}x (R$ {curr_price:.2f}) = R$ {val:.2f}")
        else:
            lines.append("Nenhuma ação em carteira.")

        total_patrimony = player.cash + total_invested
        lines.append("----------------")
        lines.append(f"💰 Patrimônio Total: R$ {total_patrimony:.2f}")
        
        div_score = player.diversification_score()
        if div_score <= 1:
            lines.append("\n⚠️ Dica: Diversifique! Compre ações de setores diferentes.")
        else:
            lines.append("\n✅ Boa! Sua carteira está diversificada.")

        return "\n".join(lines)

    def ranking(self) -> str:
   
        raw_players = database.get_all_players_data()
        
        if not raw_players:
            return "Ninguém entrou no torneio ainda."

        players_objects = []
        for p_data in raw_players:
            p = Player.from_dict(p_data)
            players_objects.append(p)

       
        top_10 = heapq.nlargest(10, players_objects, key=lambda p: p.total_equity())

        lines = ["🏆 *TOP 10 - CARTOLA XP* 🏆\n"]
        for i, p in enumerate(top_10, start=1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}º"
            lines.append(f"{medal} *{p.name}*: R$ {p.total_equity():.2f}")

        return "\n".join(lines)