import json

from jurajis_daz_material_importer.utils.slugify import slugify

INDENT = "    "

from collections import defaultdict
from typing import Any, Callable


class Node:
    def __init__(self, name: str, full_path: str = ""):
        self.name = name
        self.full_path = full_path
        self.children = []  # preserve insertion order

    def add_child(self, child: "Node"):
        self.children.append(child)


def build_tree(data: dict[str, list[dict]]) -> Node:
    root = Node("", "")
    nodes = {"": root}

    for path in data:
        parts = path.strip("/").split("/")
        current_path = ""
        parent_node = root

        for part in parts:
            current_path = f"{current_path}/{part}" if current_path else f"/{part}"
            if current_path not in nodes:
                node = Node(part, current_path)
                nodes[current_path] = node
                parent_node.add_child(node)
            parent_node = nodes[current_path]

    return root


def walk_tree(node: Node, visit_fn: Callable[[Node], None]):
    if node.full_path:
        visit_fn(node)
    for child in node.children:
        walk_tree(child, visit_fn)


def print_group_input_vars(property_groups: dict[str, dict], skip: list[str]):
    for group, properties in property_groups.items():
        if group in skip:
            continue

        group_label = group.replace("/", " ").strip()
        print(f"{INDENT}# {group_label}")

        for prop in properties:
            # Value socket
            label = slugify(prop["id"])
            print(f"{INDENT}in_{label} = \"{prop['id']}\"")
            # Map Socket (optional)
            if prop["uses_map"]:
                line = f"{INDENT}in_{label}_map = \"{prop['id']} Map\""
                print(line)

        print()


def print_group_sockets(property_groups: dict[str, list[dict]], skip: list[str]):
    panels: list[(str, str)] = []
    property_lines: list[str] = []

    def parse_level(level: Node):
        if level.full_path in skip or not level.full_path in property_groups:
            return

        group_label = level.full_path.replace("/", " ").strip()
        panel_slug = f"panel_{slugify(group_label)}"
        panels.append((panel_slug, group_label))

        property_lines.append(f"# Sockets: {group_label}")
        properties = property_groups[level.full_path]

        for prop in properties:
            label = slugify(prop["id"])

            # Value socket
            line = None
            if prop["type"] == "color":
                if prop["default_value"] != [1, 1, 1]:
                    def_value = tuple([*[float(c) for c in prop["default_value"]], 1.0])
                    line = f"sock_{label} = self._color_socket(self.in_{label}, {def_value}, parent={panel_slug})"
                else:
                    line = f"sock_{label} = self._color_socket(self.in_{label}, parent={panel_slug})"
            if prop["type"] == "float":
                if prop["default_value"] != 0:
                    def_value = prop["default_value"]
                    line = f"sock_{label} = self._float_socket(self.in_{label}, {def_value}, parent={panel_slug})"
                else:
                    line = f"sock_{label} = self._float_socket(self.in_{label}, parent={panel_slug})"
            if prop["type"] == "bool":
                if prop["default_value"]:
                    line = f"sock_{label} = self._bool_socket(self.in_{label}, True, parent={panel_slug})"
                else:
                    line = f"sock_{label} = self._bool_socket(self.in_{label}, parent={panel_slug})"
            if prop["type"] == "enum":
                value_str = ", ".join(f"{i}: {v}" for i, v in enumerate(prop["enum_opts"]))
                if prop["default_value"] != 0:
                    line = f"sock_{label} = self._float_socket(self.in_{label}, {prop['default_value']}, parent={panel_slug})  # {value_str}"
                else:
                    line = f"sock_{label} = self._float_socket(self.in_{label}, parent={panel_slug})  # {value_str}"

            if line is not None:
                property_lines.append(line)

            # Map Socket (optional)
            if prop["uses_map"]:
                line = f"sock_{label}_map = self._color_socket(self.in_{label}_map, parent={panel_slug})"
                property_lines.append(line)

        property_lines.append("")

    tree = build_tree(property_groups)
    walk_tree(tree, parse_level)

    for slug, p_label in panels:
        print(f"{INDENT}{INDENT}{slug} = self._add_panel(\"{p_label}\")")

    print()

    for property_line in property_lines:
        print(f"{INDENT}{INDENT}{property_line}")


if __name__ == '__main__':
    with open("../shader-properties/iray_uber.json") as f:
        mapping = json.load(f)

    skip_groups = [
        "/General",
        "/Geometry/Lines"
    ]

    # print_group_input_vars(mapping, skip_groups)
    print_group_sockets(mapping, skip_groups)
