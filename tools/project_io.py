import os
import pickle
from datetime import datetime

def create_project_dir(project_name: str, base_path: str = "./projects") -> str:
    """
    Crée un dossier pour le projet avec horodatage si le nom est déjà utilisé.
    """
    os.makedirs(base_path, exist_ok=True)
    project_path = os.path.join(base_path, project_name)
    if os.path.exists(project_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_path += f"_{timestamp}"
    os.makedirs(project_path, exist_ok=True)
    return project_path

def save_project_state(team_instance, path: str):
    """
    Sauvegarde l'état complet de la team (agents, mémoire, messages, etc.) dans un fichier pickle.
    """
    filepath = os.path.join(path, "project_state.pkl")
    with open(filepath, "wb") as f:
        pickle.dump(team_instance, f)
    print(f"✅ Sauvegarde du projet effectuée dans {filepath}")

def load_project_state(path: str):
    """
    Charge l'état de la team à partir du fichier pickle.
    """
    filepath = os.path.join(path, "project_state.pkl")
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"❌ Fichier introuvable : {filepath}")
    with open(filepath, "rb") as f:
        team_instance = pickle.load(f)
    print(f"📦 Projet restauré depuis {filepath}")
    return team_instance

def save_code_file(filename: str, code: str, project_path: str):
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    file_path = os.path.join(project_path, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"[INFO] Code sauvegardé dans : {file_path}")