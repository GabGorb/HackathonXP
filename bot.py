# bot.py
from ai_narrator import gerar_narracao  # <--- IMPORTANTE: Importa a função da IA
from typing import Tuple
from game_engine import Tournament, ASSETS

# Instancia o Torneio
tournament = Tournament(
    name="Cartola XP",
    days_duration=7,
    initial_cash=100000.0, # R$ 100k inicial
    max_players=None
)

def help_message() -> str:
    return (
        "🤖 *Bem-vindo ao Cartola XP!*\n\n"
        "Comandos disponíveis:\n"
        "✅ *entrar [Seu Nome]* → Entrar no jogo\n"
        "📈 *comprar [ATIVO] [QTD]* → Ex: comprar PETR4 100\n"
        "📉 *vender [ATIVO] [QTD]* → Ex: vender VALE3 50\n"
        "💰 *carteira* → Ver seu saldo e ações\n"
        "🏆 *ranking* → Ver quem está ganhando\n"
        "📋 *ativos* → Ver lista de ações\n"
        "❓ *ajuda* → Ver esta mensagem"
    )

def assets_message() -> str:
    lines = ["📋 *Ativos disponíveis (Preço Atual):*"]
    for ticker, price in ASSETS.items():
        # Tenta pegar preço real se possível, senão usa o base
        lines.append(f"• {ticker}: R$ {price:.2f}")
    return "\n".join(lines)

def parse_command(phone: str, message_body: str) -> str:
    """
    Recebe a mensagem do WhatsApp e decide o que fazer.
    """
    parts = message_body.strip().split()
    if not parts:
        return "Mande um comando. Digite *ajuda* para ver as opções."

    cmd = parts[0].lower()

    # --- Comandos ---

    if cmd in ["oi", "olá", "ola", "start", "começar", "ajuda"]:
        return help_message()

    if cmd == "entrar":
        # Ex: entrar Victor
        if len(parts) < 2:
            return "⚠️ Use: *entrar SeuNome*\nEx: entrar Matheus"
        name = " ".join(parts[1:])
        try:
            # CORREÇÃO: Usar add_player em vez de join_player
            player = tournament.add_player(phone, name=name)
            return (
                f"🎮 Bem-vindo, *{player.name}*!\n"
                f"Seu saldo inicial: R$ {player.cash:.2f}\n"
                f"Já pode comprar ações! Digite *ativos* para ver a lista."
            )
        except Exception as e:
            return f"Erro ao entrar: {str(e)}"

    if cmd == "ativos":
        return assets_message()

    if cmd == "carteira":
        return tournament.portfolio_summary(phone)

    if cmd == "ranking":
        # --- ALTERAÇÃO AQUI: Chama o Narrador IA ---
        texto_ranking = tournament.ranking()
        
        # Chama a função do arquivo ai_narrator.py
        narracao = gerar_narracao(texto_ranking)
        
        # Junta o ranking com a narração
        return f"{texto_ranking}\n\n{narracao}"

    if cmd == "comprar":
        # Ex: comprar PETR4 100
        if len(parts) < 3:
            return "⚠️ Use: *comprar [ATIVO] [QTD]*\nEx: comprar PETR4 100"
        
        ticker = parts[1].upper()
        try:
            qty = int(parts[2])
        except ValueError:
            return "⚠️ A quantidade precisa ser um número."
        
        return tournament.buy(phone, ticker, qty)

    if cmd == "vender":
        # Ex: vender PETR4 100
        if len(parts) < 3:
            return "⚠️ Use: *vender [ATIVO] [QTD]*\nEx: vender PETR4 100"
        
        ticker = parts[1].upper()
        try:
            qty = int(parts[2])
        except ValueError:
            return "⚠️ A quantidade precisa ser um número."
        
        return tournament.sell(phone, ticker, qty)

    # Se não entendeu nada
    return "Não entendi. Digite *ajuda* para ver os comandos."