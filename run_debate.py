from teams.debate_team import DebateTeam

schema_db = """
CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    origine TEXT,
    destinataire TEXT,
    type_message TEXT, -- colonne ajoutée
    contenu TEXT,
    importance INTEGER,
    memoriser BOOLEAN,
    dialogue BOOLEAN,
    affichage_force BOOLEAN,
    action TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

equipe_debat = DebateTeam.from_cli(schema_db=schema_db)
equipe_debat.envoyer_consigne_team("Discutez du réchauffement climatique")
equipe_debat.cloturer()
