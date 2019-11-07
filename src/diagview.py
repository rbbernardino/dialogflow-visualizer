#! /usr/bin/env python3
"""
Generates a graph to visualize a Dialogflow chat from the exported agent. If
an intent resolves with a fufillment, it will be necessary to provide an
association file with all output contexts for each of those intents.

    ./diagview.py <AGENT_DIR> [-f <FUFILL_INTENT_MAP>]
    INPUT:
        <AGENT_DIR>   - agent exported directory
"""

import argparse
from pathlib import Path
from graphviz import Digraph
import json
import re


class Intent:
    def __init__(self, id, name, in_contextlist, out_contextlist):
        self.id = id
        self.name = name
        self.in_contextlist = in_contextlist
        self.out_contextlist = out_contextlist


def validate_dir(dir_path: Path):
    if not dir_path.is_dir():
        print('ERROR: \'{}\' is not a valid directory'.format(dir_path))
        exit(1)


def validate_file(file_path: Path):
    if not file_path.is_file():
        print('ERROR: \'{}\' is not a valid file'.format(file_path))
        exit(1)


def prepare_outdir(outdir_path: Path):
    if outdir_path.exists():
        if outdir_path.is_file():
            print('ERROR: output path is a file')
    else:
        outdir_path.mkdir(parents=True)


# def process_agent(agent_dir: Path):


# def process_agent(agent_dir: Path, fufill_map: Path):
    

# def process_agent(agent_dir: Path, fufill_map: Path):
    

def process_agent(agent_dir: Path):
    intent_dir = Path(agent_dir / "intents")
    all_intents_files = list(intent_dir.glob("*.json"))
    f: Path
    intents_usersay_files = [f for f in all_intents_files if f.name.endswith("_usersays_pt-br.json")]
    intents_files = [f for f in all_intents_files if not f.name.endswith("_usersays_pt-br.json")]

    intent_list = []
    context_dict = {} # Key: context_id --> Value: list of intent ids
    for intent_file in intents_files:
        intent_json = json.load(open(str(intent_file)))
        out_contextlist = [c['name'] for c in intent_json['responses'][0]['affectedContexts']]
        intent_id = intent_json['id']
        intent_name = intent_json['name']
        intent_contextlist = intent_json['contexts']
        for context in intent_contextlist:
            if not (context in context_dict.keys()):
                context_dict[context] = []
            context_dict[context].append(intent_id)
        intent_list.append(Intent(intent_id, intent_name, intent_contextlist, out_contextlist))

    intent_graph = Digraph(comment="Monica Agent")
    for cur_intent in intent_list:
        intent_graph.node(cur_intent.id, cur_intent.name)
        for context in cur_intent.out_contextlist:
            for next_intent_id in context_dict[context]:
                if next_intent_id == cur_intent.id:
                    continue
                intent_graph.edge(cur_intent.id, next_intent_id)
    intent_graph.render('monica_graph', view=True)


def process_files():
    n_total = len([])
    n_cur = 0
    for i in []:
        print("Done: {}/{}".format(n_cur, n_total), end='\r')
    print("doing something...")


def main():
    parser = argparse.ArgumentParser(description="""
    Generates a graph to visualize a Dialogflow chat from the exported agent. If
    an intent resolves with a fufillment, it will be necessary to provide an
    association file with all output contexts for each of those intents.
    """)

    # main parser arguments. The order is respected, so change accordingly.
    parser.add_argument('AGENT_DIR', type=str, help='arg1 filename.')
    parser.add_argument('-f', metavar='FUFILL_INTENT_MAP', type=str,
                        required=False,
                        help='file mapping intents and context')

    args = parser.parse_args()
    agent_dir = Path(args.AGENT_DIR)
    if args.f:
        fufill_intent_map = Path(args.f)

    validate_dir(agent_dir)

    if args.f:
        validate_file(fufill_intent_map)
        process_agent(agent_dir, fufill_intent_map)
    else:
        process_agent(agent_dir)


if __name__ == '__main__':
    main()
