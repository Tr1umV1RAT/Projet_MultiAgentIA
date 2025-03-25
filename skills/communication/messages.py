# skills/communication/messages.py
from dataclasses import dataclass, field
from datetime import datetime
import json

@dataclass
class Message:
    origine: str
    destinataire: str
    type_message: str = "text"      # Type de message (ex : "text", "commande", etc.)
    contenu: str = ""               # Le contenu du message
    importance: int = 1             # Importance du message (par exemple, 1 par défaut)
    memoriser: bool = True          # Indique si le message doit être sauvegardé
    dialogue: bool = True           # Indique si le message doit être diffusé dans le dialogue
    action: str = ""                # Action associée (si applicable)
    affichage_force: bool = False   # Forcer l'affichage du message (ex : dans un débat)
    version_finale: bool = False    # False = temporaire, True = définitif
    date: datetime = field(default_factory=datetime.now)
    meta: dict = field(default_factory=dict)  # Pour toute information additionnelle

    @staticmethod
    def create(data):
        """
        Convertit une entrée en une instance de Message.
        - Si data est déjà un Message, il est renvoyé tel quel.
        - Si c'est un dictionnaire, les champs sont extraits (avec valeurs par défaut si manquants).
        - Si c'est une chaîne de caractères, elle est utilisée comme contenu avec des valeurs par défaut.
        """
        if isinstance(data, Message):
            return data
        elif isinstance(data, dict):
            return Message(
                origine=data.get("origine", ""),
                destinataire=data.get("destinataire", "ALL"),
                type_message=data.get("type_message", "text"),
                contenu=data.get("contenu", ""),
                importance=data.get("importance", 1),
                memoriser=data.get("memoriser", True),
                dialogue=data.get("dialogue", True),
                action=data.get("action", ""),
                affichage_force=data.get("affichage_force", False),
                version_finale=data.get("version_finale", False),
                date=data.get("date", datetime.now()),
                meta=data.get("meta", {})
            )
        elif isinstance(data, str):
            # Dans ce cas, la chaîne représente le contenu du message avec des valeurs par défaut
            return Message(
                origine="",
                destinataire="ALL",
                contenu=data
            )
        else:
            raise ValueError("Type de données non supporté pour créer un Message.")

    def to_dict(self):
        """
        Retourne une représentation dictionnaire du message,
        ce qui peut être utile pour l'enregistrement en base ou pour la conversion en JSON.
        """
        return {
            "origine": self.origine,
            "destinataire": self.destinataire,
            "type_message": self.type_message,
            "contenu": self.contenu,
            "importance": self.importance,
            "memoriser": self.memoriser,
            "dialogue": self.dialogue,
            "action": self.action,
            "affichage_force": self.affichage_force,
            "version_finale": self.version_finale,
            "date": self.date.isoformat() if isinstance(self.date, datetime) else self.date,
            "meta": self.meta
        }

    def __str__(self):
        # Pour une impression lisible du message, en respectant l'ordre et les informations importantes.
        return f"[{self.date.strftime('%Y-%m-%d %H:%M:%S')}] {self.origine} -> {self.destinataire}: {self.contenu}"
