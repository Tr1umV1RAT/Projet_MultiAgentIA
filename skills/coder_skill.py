from skills.llm_skill import LLMSkill

class CoderSkill(LLMSkill):
    def __init__(self, agent_name, memory=None):
        super().__init__(
            agent_name,
            role="Tu es un codeur expert. Écris uniquement le code demandé.",
            memory=memory,
        )

    def format_output(self, llm_output, original_message):
        # Ici on pourrait parser du code, structurer, extraire des blocs
        return Message(
            role=self.agent_name,
            content=llm_output.strip(),
            type="code",
            metadata={"language": "python", "response_to": original_message.id}
        )
