import re


def translate_node_id_to_blender_name(node_id: str) -> str:
    match = re.match(r'^(.*)-(\d+)$', node_id)
    if match:
        base_name = match.group(1)
        idx = int(match.group(2)) - 1
        return f'{base_name}.{idx:03d}'
    return node_id
