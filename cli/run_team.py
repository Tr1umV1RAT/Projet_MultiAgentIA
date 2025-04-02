import argparse
from cli.agent_factory import AgentFactory

def main():
    parser = argparse.ArgumentParser(description="Lancement d'une équipe/agent")
    parser.add_argument("prompt", type=str, help="Instruction à transmettre à l'agent")
    parser.add_argument("--name", type=str, default="Agent")
    parser.add_argument("--role", type=str, default=None)
    parser.add_argument("--skills", nargs="+", default=[])
    parser.add_argument("--action", type=str, default=None)

    args = parser.parse_args()

    agent = AgentFactory.create(name=args.name, role=args.role, skills=args.skills)
    metadata = {"action": args.action} if args.action else {}

    from skills.communication.messages import Message
    msg = Message(origine="cli", destinataire=args.name, contenu=args.prompt, metadata=metadata)

    response = agent.receive_message(msg)
    print(f"\n🔁 Réponse :\n{response.contenu}")

if __name__ == "__main__":
    main()
