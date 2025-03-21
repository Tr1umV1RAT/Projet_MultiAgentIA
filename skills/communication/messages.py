from dataclasses import dataclass, field
from typing import Any, Dict, Union, List

@dataclass
class Message:
    """Représente un message échangé entre agents.
    
    Chaque message peut contenir un prompt, une réflexion ou le résultat d'un outil.
    Les meta-données supplémentaires sont stockées dans 'meta'.
    """
    expediteur: str
    destinataire: Union[str, List[str]]  # Nom de l'agent destinataire, liste de noms, ou "ALL" pour diffusion globale.
    contenu: str                       # Contenu du message (texte, informations, résultat, etc.)
    dialogue: bool = False             # True si le message est de type dialogue (visible par les autres agents)
    affichage_force: bool = False      # True si le message doit être affiché en mode debug/verbose.
    meta: Dict[str, Any] = field(default_factory=dict)  # Dictionnaire de meta-données supplémentaires.
