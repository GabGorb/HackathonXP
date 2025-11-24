import os
from groq import Groq
import textwrap

try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    AI_AVAILABLE = True
except Exception as e:
    print(f"Erro ao iniciar Groq: {e}")
    AI_AVAILABLE = False

def gerar_narracao(texto_ranking: str) -> str:
    """
    Recebe o texto do ranking e gera um comentário estilo Galvão Bueno/André Henning.
    """
    if not AI_AVAILABLE or not os.getenv("GROQ_API_KEY"):
        return "🎙️ (A IA não está configurada corretamente. Verifique o .env)"

    prompt_text = f"""
    Aja como um narrador de futebol brasileiro MUITO empolgado e exagerado (estilo rádio esportiva).
    
    Abaixo está o Ranking atual do 'Cartola de Investimentos'.
    Sua missão:
    1. Identifique quem é o Líder e quem é o Lanterna.
    2. Faça um comentário curto (máximo 3 linhas) e engraçado.
    3. Use gírias de futebol ("tá na zona de rebaixamento", "pedalada fiscal", "gol de placa").
    4. NÃO repita a lista, apenas comente.
    
    RANKING ATUAL:
    {texto_ranking}
    """
    
    prompt_limpo = textwrap.dedent(prompt_text)

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt_limpo,
                }
            ],
            model="llama-3.3-70b-versatile", 
            temperature=0.8,
        )
        return "🎙️ " + chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Erro na IA: {e}")
        return "🎙️ (O narrador ficou sem voz! Erro na conexão com a IA.)"