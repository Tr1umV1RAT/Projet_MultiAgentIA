from dataclasses import dataclass, field
from typing import Any, Dict, Union, List
from config import DEFAULT_AFFICHAGE_FORCE

@dataclass
class Message:
    """
    Représente un message échangé entre agents.
    Tout échange (réflexion, résultat d'outil, consigne) se fait sous forme d'objet Message.
    """
    expediteur: str
    destinataire: Union[str, List[str]]  # Nom d'agent, liste ou "ALL" pour broadcast.
    contenu: str
    dialogue: bool = False             # Indique si le message est de type dialogue (visible publiquement)
    affichage_force: bool = DEFAULT_AFFICHAGE_FORCE  # Valeur par défaut, configurable via config.
    meta: Dict[str, Any] = field(default_factory=dict)  # Meta-données additionnelles.

    @classmethod
    def create(cls, expediteur: str, destinataire: Union[str, List[str]], contenu: str,
               dialogue: bool = False, affichage_force: bool = None, meta: Dict[str, Any] = None):
        if affichage_force is None:
            from config import DEFAULT_AFFICHAGE_FORCE
            affichage_force = DEFAULT_AFFICHAGE_FORCE
        if meta is None:
            meta = {}
        return cls(expediteur=expediteur, destinataire=destinataire, contenu=contenu,
                   dialogue=dialogue, affichage_force=affichage_force, meta=meta)
