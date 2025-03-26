from dataclasses import dataclass, field, asdict
from datetime import datetime
import uuid
import json

@dataclass
class Message:
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    origine: str = ""
    destinataire: str = ""
    type_message: str = "text"
    contenu: str = ""
    importance: int = 1
    memoriser: bool = True
    dialogue: bool = True
    action: str = ""
    affichage_force: bool = False
    version_finale: bool = False
    date: datetime = field(default_factory=datetime.now)
    meta: dict = field(default_factory=dict)
    conversation_id: str = ""

    # ---- FACTORY ----
    @staticmethod
    def create(data):
        """
        Crée un Message à partir :
        - d'une instance Message (copie)
        - d'un dict contenant les champs
        """
        if isinstance(data, Message):
            return data
        elif isinstance(data, dict):
            return Message(
                id=data.get("id", uuid.uuid4().hex),
                origine=data.get("origine", ""),
                destinataire=data.get("destinataire", ""),
                type_message=data.get("type_message", "text"),
                contenu=data.get("contenu", ""),
                importance=int(data.get("importance", 1)),
                memoriser=bool(data.get("memoriser", True)),
                dialogue=bool(data.get("dialogue", True)),
                action=data.get("action", ""),
                affichage_force=bool(data.get("affichage_force", False)),
                version_finale=bool(data.get("version_finale", False)),
                date=datetime.fromisoformat(data["date"]) if "date" in data else datetime.now(),
                meta=data.get("meta", {}) if isinstance(data.get("meta", {}), dict) else json.loads(data.get("meta", "{}")),
                conversation_id=data.get("conversation_id", "")
            )
        else:
            raise TypeError("Message.create() n'accepte que des dicts ou des objets Message.")

    # ---- VALIDATION ----
    def is_valid(self) -> bool:
        return bool(self.origine and self.destinataire and self.contenu)

    # ---- DICT / JSON ----
    def to_dict(self):
        data = asdict(self)
        data["date"] = self.date.isoformat()
        data["meta"] = json.dumps(self.meta)
        return data

    @staticmethod
    def from_dict(data: dict):
        data["date"] = datetime.fromisoformat(data["date"])
        data["meta"] = json.loads(data["meta"])
        return Message(**data)

    def to_json(self) -> str:
        """
        Sérialise le message en JSON. Nettoie les types non sérialisables.
        """
        def default_serializer(obj):
            if isinstance(obj, type):
                return obj.__name__
            try:
                return str(obj)
            except Exception:
                return "[Unserializable]"

        return json.dumps(self.to_dict(), default=default_serializer)

    # ---- REPRÉSENTATION ----
    def __repr__(self):
        return f"<Message {self.type_message.upper()} {self.origine} → {self.destinataire} | {self.date:%H:%M:%S}>"

    # ---- HELPERS PAR TYPE ----
    @staticmethod
    def code(expediteur, destinataire, contenu, importance=5, **kwargs):
        return Message(
            origine=expediteur,
            destinataire=destinataire,
            type_message="code",
            contenu=contenu,
            importance=importance,
            **kwargs
        )

    @staticmethod
    def erreur(expediteur, destinataire, contenu, **kwargs):
        return Message(
            origine=expediteur,
            destinataire=destinataire,
            type_message="erreur",
            contenu=contenu,
            importance=10,
            dialogue=False,
            **kwargs
        )

    @staticmethod
    def system(expediteur, destinataire, contenu, **kwargs):
        kwargs.setdefault("type_message", "system")
        kwargs.setdefault("dialogue", False)
        kwargs.setdefault("memoriser", False)
        kwargs.setdefault("importance", 2)
        return Message(
            origine=expediteur,
            destinataire=destinataire,
            contenu=contenu,
            **kwargs
        )