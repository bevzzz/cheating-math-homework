import weaviate
from weaviate.collections.classes.config import Configure, DataType, Property, VectorDistances
from weaviate.collections.classes.data import DataObject
from weaviate.collections.classes.filters import Filter

import collection

WORDS = "Words"

def find_least_similar(client: weaviate.WeaviateClient, word_list: list[str]) -> str:
    """Find the word that does not belong to the list."""
    collection.setup(client, WORDS,
        properties=[Property(name="word", data_type=DataType.TEXT)],
        vectorizer_config=Configure.Vectorizer.text2vec_contextionary(vectorize_collection_name=False),
    )
    _store_words(client, word_list)

    words = client.collections.get(WORDS)

    # We want to fetch all but the one "nearest" match for the word.
    # The result set should not include the search term itself.
    limit = len(word_list) - 2

    scores: dict[str, int] = {word: 0 for word in word_list}
    for word in word_list:
        knn = words.query.near_text(
            query=word,
            limit=limit,
            filters=Filter.by_property("word").not_equal(word),
            return_properties=["word"]
        )
        if knn is None:
            continue

        for neighbour in knn.objects:
            w = str(neighbour.properties["word"])
            scores[w] = scores[w] + 1

    return min(scores, key=lambda k: scores.get(k, 0))


def _store_words(client: weaviate.WeaviateClient, word_list: list[str]):
    """Store input words in the Words collection."""
    data_objects = list()
    for word in word_list:
        data_objects.append(DataObject(
            properties={"word": word},
        ))

    words = client.collections.get("Words")
    words.data.insert_many(data_objects)


def add_subcommand(command_name: str, cli: any)-> None:
    """Add subcommand and flags to the argument parser."""
    
    parser = cli.add_parser("words")
    parser.add_argument("words", nargs="*", type=str)
