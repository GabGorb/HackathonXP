# database.py
import os
import firebase_admin
from firebase_admin import credentials, firestore

CRED_FILE = "firebase_credentials.json"

def get_db():
    """
    Inicializa a conexão com o Firebase (Padrão Singleton)
    """
    if not firebase_admin._apps:
        if os.path.exists(CRED_FILE):
            cred = credentials.Certificate(CRED_FILE)
            firebase_admin.initialize_app(cred)
            print("🔥 Firebase conectado com sucesso!")
        else:
            print(f"⚠️ ERRO: Arquivo '{CRED_FILE}' não encontrado. O jogo não salvará dados.")
            return None
    
    return firestore.client()


def save_player_data(phone: str, data: dict):
    """
    Salva ou atualiza os dados do jogador no Firestore.
    """
    db = get_db()
    if db:
        db.collection("players").document(phone).set(data)

def get_player_data(phone: str) -> dict:
    """
    Busca os dados de um jogador pelo telefone.
    Retorna um dicionário ou None se não existir.
    """
    db = get_db()
    if db:
        doc = db.collection("players").document(phone).get()
        if doc.exists:
            return doc.to_dict()
    return None

def get_all_players_data() -> list:
    """
    Retorna uma lista com os dados de todos os jogadores.
    Útil para montar o ranking.
    """
    db = get_db()
    players = []
    if db:
        docs = db.collection("players").stream()
        for doc in docs:
            players.append(doc.to_dict())
    return players