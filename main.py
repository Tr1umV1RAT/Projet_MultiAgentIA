from agents import BaseAgent
from roles.climato_sceptique import ClimatoSceptique
from roles.scientifique import Scientifique
from skills.communication.messages import Message
from skills.db_management.db_management import DBManagementSkill
from teams.base_team import BaseTeam
from config import Config

Config.verbose = True

schema_memory = """
CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    origine TEXT,
    destinataire TEXT,
    type_message TEXT,
    contenu TEXT,
    importance INTEGER,
    memoriser BOOLEAN,
    dialogue BOOLEAN,
    action TEXT,
    affichage_force BOOLEAN,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

bob = BaseAgent("Bob", ClimatoSceptique())
jean = BaseAgent("Jean", Scientifique())

equipe_debat = BaseTeam("Débat_Climat", [bob, jean], schema_db=schema_memory)

# Envoie explicite d'une consigne claire :
equipe_debat.envoyer_consigne_team("Discutez du réchauffement climatique.")
equipe_debat.agents[0].communication.recevoir(bob)
equipe_debat.agents[1].communication.recevoir(equipe_debat.agents[1])

