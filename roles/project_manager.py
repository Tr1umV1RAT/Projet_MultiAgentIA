from roles.base_role import BaseRole
from tools.llm_adapter import LLMAdapterTool

class ProjectManagerRole(BaseRole):
    def __init__(self):
        super().__init__(
            nom_role="ProjectManager",
            objectif="Planifier, coordonner et distribuer clairement les tâches d’un projet complexe.",
            contexte="""
Tu es un chef de projet rigoureux, chargé de structurer un travail complexe en tâches claires, bien définies,
réalisables et cohérentes avec les objectifs globaux du projet.

Tu interagis avec les autres membres pour clarifier les exigences, anticiper les problèmes, et proposer des étapes concrètes.
""",
            outils=[LLMAdapterTool()],
            instructions_specifiques="""
Utilise tes connaissances pour créer un plan clair et détaillé. Divise le projet en sous-tâches ordonnées.
Tu peux proposer un plan d'action, une arborescence logique, ou une roadmap si utile.
"""
        )
