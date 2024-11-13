import argparse

def calculate_distance(v1: tuple[float, ...], v2: tuple[float, ...]) -> float:
    pass


def list_float(str_list: str, sep: str) -> tuple[float, ...]:
    """Parse stringified array like [1,2,3] to list of floats."""

    str_list = str_list.strip("[").strip("]")
    items = str_list.split(sep)
    return tuple(float(i) for i in items)


def run(args: argparse.Namespace):

    v1, v2 = list_float(args.v1, args.sep), list_float(args.v2, args.sep)
    distance = calculate_distance(v1, v2)
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
