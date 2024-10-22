import sys
from storage.vector import ask as vector_ask
import asyncio

async def ask(query: str) -> str:
    answer = await vector_ask(query)
    return answer

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ask.py <query>")
        sys.exit(1)

    query = sys.argv[1]
    answer = asyncio.run(ask(query))
    print(answer)
