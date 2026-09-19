import json
import os
import re


# Find the main EcoMind project folder
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# Location of biodiversity knowledge base
KNOWLEDGE_FILE = os.path.join(
    BASE_DIR,
    "data",
    "biodiversity_knowledge.json"
)


# Load the knowledge base
def load_knowledge_base():
    try:
        with open(
            KNOWLEDGE_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except Exception as error:
        print("Knowledge base loading error:", error)
        return []


# Convert text into searchable words
def tokenize(text):
    text = str(text).lower()

    return set(
        re.findall(
            r"\b[a-zA-Z0-9]+\b",
            text
        )
    )


# Retrieve the most relevant knowledge
def retrieve_knowledge(query, top_k=3):

    knowledge_base = load_knowledge_base()

    query_words = tokenize(query)

    results = []


    # Check every document in the knowledge base
    for item in knowledge_base:

        searchable_text = " ".join([
            item.get("topic", ""),
            item.get("condition", ""),
            item.get("evidence", ""),
            item.get("recommendation", ""),
            item.get("reasoning", ""),
            " ".join(item.get("keywords", []))
        ])


        document_words = tokenize(
            searchable_text
        )


        # Find matching words
        matches = query_words.intersection(
            document_words
        )


        # Basic relevance score
        score = len(matches)


        # Give extra importance to matching topics
        topic = item.get(
            "topic",
            ""
        ).lower()


        if topic and topic in query.lower():
            score += 5


        # Give extra importance to matching keywords
        for keyword in item.get(
            "keywords",
            []
        ):

            if str(keyword).lower() in query.lower():
                score += 3


        # Add useful documents to results
        if score > 0:

            results.append({
                "score": score,

                "id": item.get("id"),

                "topic": item.get("topic"),

                "condition": item.get("condition"),

                "evidence": item.get("evidence"),

                "recommendation": item.get(
                    "recommendation"
                ),

                "affected_metrics": item.get(
                    "affected_metrics",
                    []
                ),

                "reasoning": item.get(
                    "reasoning"
                ),

                "source": item.get(
                    "source"
                ),

                "source_url": item.get(
                    "source_url"
                )
            })


    # Sort highest relevance first
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    # Return only the best results
    return results[:top_k]


# Build a search query from environmental data
def build_query(data):

    return " ".join([
        data.get("species", ""),
        data.get("location", ""),
        str(data.get("ph", "")),
        str(data.get("organic_carbon", "")),
        str(data.get("soil_moisture", "")),
        str(data.get("temperature", "")),
        str(data.get("rainfall", "")),
        data.get("land_use", "")
    ])


# Test the RAG retrieval system
if __name__ == "__main__":

    test_query = (
        "low soil organic carbon "
        "monoculture pollinators "
        "biodiversity habitat"
    )


    results = retrieve_knowledge(
        test_query
    )


    print()
    print("EcoMind RAG Retrieval Test")
    print("=" * 40)


    for result in results:

        print(
            f"\nTopic: {result['topic']}"
        )

        print(
            f"Score: {result['score']}"
        )

        print(
            f"Evidence: {result['evidence']}"
        )

        print(
            f"Recommendation: "
            f"{result['recommendation']}"
        )

        print(
            f"Source: {result['source']}"
        )

        print(
            f"URL: {result['source_url']}"
        )