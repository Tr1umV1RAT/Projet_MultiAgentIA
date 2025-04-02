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
    metadata: dict = field(default_factory=dict)
    conversation_id: str = field(default_factory=lambda: uuid.uuid4().hex)

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
                metadata=data.get("metadata", {}) if isinstance(data.get("metadata", {}), dict) else json.loads(data.get("metadata", "{}")),
                conversation_id=data.get("conversation_id", uuid.uuid4().hex)
            )
        else:
            raise TypeError("Message.create() accepte uniquement des dicts ou des objets Message.")

    # ---- VALIDATION ----
    def is_valid(self) -> bool:
        return bool(self.origine and self.destinataire and self.contenu)

    # ---- DICT / JSON ----
    def to_dict(self):
        data = asdict(self)
        data["date"] = self.date.isoformat()
        data["metadata"] = json.dumps(self.metadata)
        return data

    @staticmethod
    def from_dict(data: dict):
        data["date"] = datetime.fromisoformat(data["date"])
        data["metadata"] = json.loads(data["metadata"])
        return Message(**data)

    def to_json(self) -> str:
        """
        Sérialise le message en JSON en gérant les types non sérialisables.
        """
        def default_serializer(obj):
            if isinstance(obj, (datetime,)):
                return obj.isoformat()
            if isinstance(obj, uuid.UUID):
                return str(obj)
            return str(obj)

        return json.dumps(self.to_dict(), default=default_serializer)

    # ---- REPRÉSENTATION ----
    def __repr__(self):
        return f"<Message [{self.type_message.upper()}] {self.origine} → {self.destinataire} | {self.date:%Y-%m-%d %H:%M:%S}>"

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
            memoriser=True,
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
    def copy_for(self, destinataire: str, metadata: dict = None):
            new_metadata = self.metadata.copy() if self.metadata else {}
            if metadata:
                new_metadata.update(metadata)

            return Message(
                origine=self.destinataire,
                destinataire=destinataire,
                contenu=self.contenu,
                type_message=self.type_message,
                importance=self.importance,
                memoriser=self.memoriser,
                dialogue=self.dialogue,
                action="",  # on force à passer par metadata
                affichage_force=self.affichage_force,
                version_finale=self.version_finale,
                conversation_id=self.conversation_id,
                metadata=new_metadata
            )
