from sentence_transformers import SentenceTransformer
import psutil
import os

process = psutil.Process(os.getpid())

print(
    "Before:",
    process.memory_info().rss / 1024 / 1024
)

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

model.encode(
    ["hello world"]
)

print(
    "After:",
    process.memory_info().rss / 1024 / 1024
)