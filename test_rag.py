from src.pipeline import ask

query = "How do I cancel my subscription?"
result = ask(query)

print("Question:")
print(result["query"])
print("\nAnswer:")
print(result["answer"])
print("\nSources:")
for s in result["sources"]:
    print("-", s)