import sys
from storage.vector import ask as vector_ask

def ask(query: str) -> str:
    answer = vector_ask(query)
    return answer

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ask.py <query>")
        sys.exit(1)

    query = sys.argv[1]
    answer = ask(query)
    print(answer)
