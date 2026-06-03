from dotenv import load_dotenv
load_dotenv()

import os
import voyageai

client = voyageai.Client(
    api_key=os.getenv("VOYAGE_API_KEY")
)

result = client.embed(
    ["hello world"],
    model="voyage-3-lite"
)

print(
    "Dimension:",
    len(result.embeddings[0])
)