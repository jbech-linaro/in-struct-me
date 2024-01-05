#!/usr/bin/env python

import argparse
import os
import sys
import re
from collections import defaultdict


def my_parser():
    parser = argparse.ArgumentParser(
        description='In-struct-me',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '-g', '--grep',
        default="",
        required=False,
        help='Highlight items matching this')

    parser.add_argument(
        '-v', '--verbose',
        default=False,
        required=False,
        action='store_true',
        help='Show struct content')

    parser.add_argument(
        "path",
        help="Source location")

    return parser.parse_args()


def remove_comments(file_content):
    # Remove C-style comments (/* ... */)
    file_content = re.sub(r'/\*.*?\*/', '', file_content, flags=re.DOTALL)

    # Remove C++-style comments (// ...)
    file_content = re.sub(r'//.*?$', '', file_content, flags=re.MULTILINE)

    return file_content


def extract_structs(file_content):
    file_content = remove_comments(file_content)
    structs = defaultdict(list)

    # Define a regular expression to match structs in the file content
    struct_pattern = re.compile(r'struct\s+(\w+)\s*{([^}]*)}', re.DOTALL)
    matches = struct_pattern.findall(file_content)

    for match in matches:
        struct_name, struct_members = match
        struct_members_list = [
            member.strip()
            for member in struct_members.split(';')
            if member.strip()
        ]
        structs[struct_name] = struct_members_list

    return structs


def process_file(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
        return extract_structs(file_content)


def process_files(folder_path='.'):
    all_structs = defaultdict(list)
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(('.c', '.h')):
                file_path = os.path.join(root, file_name)
                file_structs = process_file(file_path)
                for struct_name, struct_members in file_structs.items():
                    all_structs[struct_name].extend(struct_members)
    return all_structs


def add_link(d, key, link, extra=None):
    if key in d:
        if link not in d[key]:
            d[key].append(link)
    else:
        d[key] = [link]


def is_ignored(struct_name, ignore_patterns):
    for pattern in ignore_patterns:
        if re.search(pattern, struct_name):
            return True
    return False


def create_dag(structs):
    struct_dict = {}

    ignore_file_path = 'ignore.txt'
    ignore_patterns = None
    with open(ignore_file_path, 'r') as ignore_file:
        ignore_patterns = [line.strip() for line in ignore_file]

    for struct_name, struct_members in structs.items():
        for s in struct_members:
            matches = re.finditer(r'\bstruct\s+(\w+)', s)
            for match in matches:
                struct_name_match = match.group(1)
                # Link the two structs together if we don't intend to ignore it
                if not is_ignored(struct_name_match, ignore_patterns):
                    add_link(struct_dict, struct_name, struct_name_match)

    return struct_dict


def truncate_label(label):
    # Truncate super long structs
    if len(label) > 256:
        label = label[:256] + "\\l" + "< ... truncated ... >"
    return label


def populate_verbose_label(node_data, key, original_dict, args):
    # All these "\\l" are here to make text left aligned.
    label = "\\l".join(original_dict[key]) + "\\l"
    # Remove multiple spaces
    label = re.sub(r'\s+', ' ', label)
    label = truncate_label(label)

    node_data += f', label="struct {key}\\l---\\l{label}"'

    return node_data


def grep_colorize(node_data, key, original_dict, args):
    set_color = False

    if args.grep in key:
        set_color = True
    else:
        for member in original_dict[key]:
            if args.grep in member:
                set_color = True

    if set_color:
        node_data += ', color="peachpuff", style="filled"'

    return node_data


def write_dot_file(args, dot_data):
    with open('dag_graph.dot', 'w') as dot_file:
        dot_file.write('digraph DAG {\n')
        if args.verbose:
            dot_file.write('graph [ rankdir = "LR", labeljust=l ];\n')
        dot_file.write('\n'.join(dot_data))
        dot_file.write('\n}')


def create_graphviz(struct_dict, original_dict, args):
    dot_data = []

    # Generate nodes
    for key in struct_dict:
        node_data = f'"{key}" [shape="box"'
        if args.verbose:
            node_data = populate_verbose_label(node_data, key, original_dict,
                                               args)
        if args.grep != "":
            node_data = grep_colorize(node_data, key, original_dict, args)

        # End the node data
        node_data += "];"
        dot_data.append(node_data)

    # Generate edges.
    for key, values in struct_dict.items():
        for value in values:
            dot_data.append(f'"{key}" -> "{value}";')

    write_dot_file(args, dot_data)
    print("DOT file 'dag_graph.dot' has been generated.")


if __name__ == "__main__":
    args = my_parser()

    if args.grep:
        print(f"grep for: {args.grep}")

    if args.verbose:
        print("Verbose enabled")

    result = process_files(args.path)
    struct_dict = create_dag(result)
    create_graphviz(struct_dict, result, args)
