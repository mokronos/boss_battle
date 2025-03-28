import dotenv

from boss_battle.boss_generation.open_router_client import OpenRouterClient

dotenv.load_dotenv()


def main():
    client = OpenRouterClient("deepseek/deepseek-r1:free")
    prompt = "I want an orc as a boss."

    try:
        structured_output = client.get_structured_output(prompt)

        print("Your boss:")
        print(structured_output.model_dump_json(indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
