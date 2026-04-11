from src.retriever import retrieve

query = "How do I cancel my plan?"
results = retrieve(query)

print("Top results:")
for r in results:
    print("-", r)