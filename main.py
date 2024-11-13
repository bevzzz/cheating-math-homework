import argparse
import weaviate
import vectors
import words

def list_float(str_list: str, sep: str) -> tuple[float, ...]:
    """Parse stringified array like [1,2,3] to list of floats."""

    str_list = str_list.strip("[").strip("]")
    items = str_list.split(sep)
    return tuple(float(i) for i in items)


def run(args: argparse.Namespace):

    with weaviate.connect_to_local() as client:
        match args.command:
            case "distance":
                v1, v2 = list_float(args.v1, args.sep), list_float(args.v2, args.sep)
                distance = vectors.calculate_distance(client, v1, v2)
                print(f"Distance: {distance}")
            case "words":
                answer = words.find_least_similar(client, args.words)
                print(f"Methinks the word '{answer}' does not belong.")


parser = argparse.ArgumentParser(
    prog="cheetah",
    description="Cheating Math Homework with Weaviate Vector Database",
    usage="cheetah <v1> <v2> [--sep] [--precision]",
)
subparsers = parser.add_subparsers(dest="command")

vectors.add_subcommand("distance", subparsers)
words.add_subcommand("words", subparsers)

if __name__ == "__main__":
    args = parser.parse_args()
    run(args)
