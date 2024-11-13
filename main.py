import argparse

import weaviate
from weaviate.collections.classes.config import Configure, VectorDistances
from weaviate.collections.classes.grpc import MetadataQuery

def calculate_distance(client: weaviate.WeaviateClient, v1: tuple[float, ...], v2: tuple[float, ...]) -> float:
    """
    Retrieve the closes vector from Givens collections
    and return its distance to the search vector.
    """
    _setup_collection(client, "Givens", vector_index_config=Configure.VectorIndex.hnsw(
      distance_metric=VectorDistances.L2_SQUARED,
    ))

    givens = client.collections.get("Givens")
    givens.data.insert({}, vector=list(v1))

    result = givens.query.near_vector(
        near_vector=list(v2),
        limit=1,
        return_metadata=MetadataQuery(distance=True),
    )
    assert len(result.objects) == 1

    distance = result.objects[0].metadata.distance
    assert distance is not None

    # Weaviate does not calculate the square root of the distances.
    return pow(distance, 0.5)


def _setup_collection(client: weaviate.WeaviateClient, name: str, **kwargs):
    """
    Create Givens collections or re-create an existing one.
    The collection will use l2-squared vectorizer to calculate Euclidean distance.
    """
    if not client.collections.exists(name):
        client.collections.create(name, **kwargs)
        return

    client.collections.delete(name)
    _setup_collection(client, name, **kwargs)

    count = sum(1 for _ in client.collections.get(name).iterator())
    assert count == 0


def list_float(str_list: str, sep: str) -> tuple[float, ...]:
    """Parse stringified array like [1,2,3] to list of floats."""

    str_list = str_list.strip("[").strip("]")
    items = str_list.split(sep)
    return tuple(float(i) for i in items)


def run(args: argparse.Namespace):

    with weaviate.connect_to_local() as client:
        v1, v2 = list_float(args.v1, args.sep), list_float(args.v2, args.sep)
        distance = calculate_distance(client, v1, v2)
        print(f"Distance: {distance}")


parser = argparse.ArgumentParser(
    prog="cheetah",
    description="Cheating Math Homework with Weaviate Vector Database",
    usage="cheetah <v1> <v2> [--sep] [--precision]",
)

parser.add_argument("v1", type=str)
parser.add_argument("v2", type=str)
parser.add_argument("--sep", default=",", help="list item separator (default: ',')")
parser.add_argument("--precision", type=int, default=None, help="round down the result to N decimal points")

if __name__ == "__main__":
    args = parser.parse_args()
    run(args)
