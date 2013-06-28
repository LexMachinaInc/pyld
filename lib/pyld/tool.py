import argparse
import sys
import json

from .jsonld import (
    to_rdf,
    from_rdf,
    JsonLdProcessor,
)


def main():
    parser = argparse.ArgumentParser(description='Process JSON-LD')
    parser.add_argument('infile', type=argparse.FileType('r'), nargs='?', default=sys.stdin)
    parser.add_argument('outfile', type=argparse.FileType('w'), nargs='?', default=sys.stdout)
    parser.add_argument('--action', choices=['to_rdf', 'from_rdf'], default='to_rdf')

    action_map = {
        'to_rdf': to_rdf,
        'from_rdf': from_rdf,
    }

    args = parser.parse_args()

    with args.infile as infile, args.outfile as outfile:
        action = action_map[args.action]
        if args.action in ['to_rdf']:
            jobj = json.load(infile)
            dataset = action(jobj)
            for graph_name, triples in dataset.items():
                for triple in triples:
                    if graph_name == '@default':
                        graph_name = None
                    quad = JsonLdProcessor.to_nquad(triple, graph_name)
                    outfile.write(quad)


if __name__ == "__main__":
    main()
