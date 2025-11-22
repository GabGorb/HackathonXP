# bot.py

from typing import Tuple
from game_engine import Tournament, ASSETS

# Cria um torneio global (MVP: só um por vez)
tournament = Tournament(
    name="Cartola de Investimentos",
    days_duration=7,
    initial_cash=10000.0,
    max_players=None,  # sem limite enquanto não configurar
)



def help_message() -> str:
    return (
        "🤖 Bem-vindo ao Cartola de Investimentos!\n\n"
        "Comandos disponíveis:\n"
        "- configurar N_JOGADORES DIAS SALDO_INICIAL → configura o torneio\n"
        "- entrar [seu_nome]                     → entrar no torneio\n"
        "- ativos                                 → listar ativos disponíveis\n"
        "- comprar TICKER QTD                     → comprar um ativo\n"
        "- vender TICKER QTD                      → vender um ativo\n"
        "- carteira                               → ver sua carteira\n"
        "- ranking                                → ver ranking do torneio\n"
        "- ajuda                                  → ver esta mensagem\n\n"
        "Exemplo config: 'configurar 10 7 50000'\n"
        "Exemplo compra: 'comprar PETR4 10'"
    )



def assets_message() -> str:
    lines = ["📋 Ativos disponíveis no torneio (preço atual):"]
    for ticker in ASSETS.keys():
        price = tournament.get_price(ticker)
        lines.append(f"- {ticker}: R$ {price:.2f}")
    lines.append("")
    lines.append("Lembre-se: diversificar ajuda a reduzir o risco 😉")
    return "\n".join(lines)




def parse_command(phone: str, text: str) -> str:
    """
    Interpreta a mensagem de texto e retorna a resposta.
    """
    text = text.strip()
    if not text:
        return "Não entendi sua mensagem. Envie 'ajuda' para ver os comandos."

    parts = text.split()
    cmd = parts[0].lower()

    # -------- comandos --------

    if cmd in ["ajuda", "help", "?"]:
        return help_message()


    if cmd in ["ajuda", "help", "?"]:
        return help_message()

    if cmd == "configurar":
        # Uso: configurar N_JOGADORES DIAS SALDO_INICIAL
        if len(parts) < 4:
            return (
                "Uso: configurar N_JOGADORES DIAS SALDO_INICIAL\n"
                "Exemplo: configurar 10 7 50000"
            )
        try:
            max_players = int(parts[1])
            days = int(parts[2])
            initial_cash = float(parts[3])
        except ValueError:
            return (
                "Parâmetros inválidos. Use números, por exemplo:\n"
                "configurar 10 7 50000"
            )

        tournament.configure(
            max_players=max_players,
            days_duration=days,
            initial_cash=initial_cash,
        )

        return (
            "🏁 Torneio configurado!\n"
            f"- Máx. jogadores: {max_players}\n"
            f"- Duração: {days} dia(s)\n"
            f"- Saldo inicial: R$ {initial_cash:.2f}\n\n"
            "Agora o pessoal pode entrar usando: entrar SeuNome"
        )


    if cmd == "entrar":
        name = " ".join(parts[1:]) if len(parts) > 1 else ""
        try:
            player = tournament.join_player(phone, name=name)
        except ValueError as e:
            # erro de limite de jogadores
            return f"⚠️ Não foi possível entrar no torneio: {e}"

        return (
            f"🎮 Você entrou no torneio, {player.name or player.phone}!\n"
            f"Saldo inicial: R$ {player.cash:.2f}.\n"
            f"Use 'ativos' para ver os ativos disponíveis."
        )


    if cmd == "ativos":
        return assets_message()

    if cmd == "carteira":
        return tournament.portfolio_summary(phone)

    if cmd == "ranking":
        return tournament.ranking()

    if cmd == "comprar":
        if len(parts) < 3:
            return "Uso: comprar TICKER QTD\nEx: comprar PETR4 10"
        ticker = parts[1].upper()
        try:
            qty = int(parts[2])
        except ValueError:
            return "Quantidade deve ser um número inteiro.\nEx: comprar PETR4 10"

        return tournament.buy(phone, ticker, qty)

    if cmd == "vender":
        if len(parts) < 3:
            return "Uso: vender TICKER QTD\nEx: vender PETR4 5"
        ticker = parts[1].upper()
        try:
            qty = int(parts[2])
        except ValueError:
            return "Quantidade deve ser um número inteiro.\nEx: vender PETR4 5"

        return tournament.sell(phone, ticker, qty)

    # Fallback: não reconheceu comando
    return (
        "Não entendi o comando. 🤔\n"
        "Envie 'ajuda' para ver a lista de comandos disponíveis."
    )
