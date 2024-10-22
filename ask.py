import sys
from storage.vector import ask

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ask.py <query>")
        sys.exit(1)

    query = sys.argv[1]
    results = ask(query)

    for result in results:
        print(result)
