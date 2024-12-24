import argparse
import re
from collections import defaultdict
from typing import Iterable


class Network:
    completed_networks: defaultdict[int, set[tuple[str, ...]]]
    nodes: defaultdict[str, set[str]]

    def __init__(self, text: str):
        cache: defaultdict[str, set[str]] = defaultdict(set)
        for m in re.finditer(r'(..)-(..)', text):
            a = m.group(1)
            b = m.group(2)
            cache[a].add(b)
            cache[b].add(a)
        self.nodes = cache
        self.completed_networks = defaultdict(set)

    def get_names(self):
        return self.nodes.keys()

    def get_largest_networks(self):
        largest_network_length = max(*self.completed_networks.keys())
        return list(self.completed_networks[largest_network_length])

    def get_complete_network_with_n_nodes(self, n: int):
        return list(self.completed_networks[n])

    def build_network_for(self, names: Iterable[str]):
        networks = self.completed_networks
        for name in names:
            name_pool = set(self.nodes[name])

            depth = 1
            work: set[tuple[str, ...]] = {(name,)}
            while work:
                next_work = set()
                for network in work:
                    # Don't bother with already explored networks
                    if network in networks[depth]: continue
                    networks[depth].add(network)

                    for next_name in name_pool.difference(network):
                        if self.nodes[next_name].issuperset(network):
                            next_work.add(tuple(sorted({*network, next_name})))
                depth += 1
                work = next_work


def solve(input_path: str, /, **_kwargs):
    with open(input_path, "r", encoding='utf-8') as file:
        input_text = file.read().strip().replace('\r', '')

    network = Network(input_text)

    names_with_t = [name for name in network.get_names() if name.startswith('t')]
    network.build_network_for(names_with_t)
    p1 = len(network.get_complete_network_with_n_nodes(3))
    print(f'p1 = {p1}')

    largest_networks = network.get_largest_networks()
    assert len(largest_networks) == 1, "p2 solution should have a single, unique answer"

    p2 = ','.join(largest_networks[0])
    print(f'p2 = {p2}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="sample.txt")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    solve(args.input, verbose=args.verbose)


if __name__ == "__main__":
    main()
