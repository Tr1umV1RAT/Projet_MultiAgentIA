from teams.code_team import CodeTeam

if __name__ == "__main__":
    prompt_initial = (
        "Nous allons développer un projet Python simple : "
        "un outil de gestion de tâches avec ajout, suppression et affichage.\n"
        "Travaillez en équipe pour proposer un plan d'action, coder la solution, relire, synthétiser."
    )

    team = CodeTeam(
        prompt_initial=prompt_initial,
        n_rounds=3,
        verbose=True,
        distribuer_prompt_initial=True
    )

    team.run()
    team.cloturer()
