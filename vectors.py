import weaviate
from weaviate.collections.classes.config import Configure, VectorDistances
from weaviate.collections.classes.grpc import MetadataQuery

import collection

GIVENS = "Givens"

def calculate_distance(client: weaviate.WeaviateClient, v1: tuple[float, ...], v2: tuple[float, ...]) -> float:
    """
    Retrieve the closest vector from Givens collections
    and return its distance to the search vector.
    """

    # The collection should use l2-squared distance metric to calculate Euclidean distance.
    collection.setup(client, GIVENS, vector_index_config=Configure.VectorIndex.hnsw(
      distance_metric=VectorDistances.L2_SQUARED,
    ))

    givens = client.collections.get(GIVENS)
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


def add_subcommand(command: str, cli: any) -> None:
    """Add subcommand and flags to the argument parser."""

    parser = cli.add_parser(command, description="CLI tool for calculating vector distance")

    parser.add_argument("v1", type=str)
    parser.add_argument("v2", type=str)
    parser.add_argument("--sep", default=",", help="list item separator")
    parser.add_argument("--precision", type=int, default=None)