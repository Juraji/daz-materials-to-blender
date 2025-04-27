from bpy.types import NodeTree, NodeGroupOutput


class NodeTreeArranger:
    """
    Heavilly based on https://github.com/JuhaW/NodeArrange.
    Just more esoteric.

    TODO: Currently not used, as node dimensions are 0 when not in view.
    Need to come up with an alternate way of determining dimensions? Without navigating the view to the node tree.
    """

    def __init__(self, margin_x: int, margin_y: int):
        self._margin_x = margin_x
        self._margin_y = margin_y
        self._average_y = 0
        self._last_x = 0

    def arrange_nodes(self, node_tree: NodeTree):
        output_nodes = [n for n in node_tree.nodes if isinstance(n, NodeGroupOutput)]

        tree = [output_nodes]

        while tree and tree[-1]:
            tree.append([
                link.from_node
                for node in tree[-1]
                for inp in node.inputs if inp.is_linked
                for link in inp.links
            ])

        # Remove empty level at the end if it exists
        if tree and not tree[-1]:
            tree.pop()

        # remove duplicate nodes at the same level, first wins
        tree = [list(set(nodes)) for nodes in tree]

        # remove duplicate nodes in all levels, last wins
        seen = set()
        for row in reversed(tree[1:]):
            row[:] = [col for col in row if col not in seen and not seen.add(col)]

        self._last_x = 0
        for l in range(0, len(tree)):
            self._average_y = 0
            nodes = [x for x in tree[l]]
            self._arrange_nodes_at_level(nodes, l)

    def _arrange_nodes_at_level(self, nodes, level: int):
        # Detach parents but remember them
        parents = [node.parent for node in nodes]
        for node in nodes:
            node.parent = None

        # Compute max width for consistent horizontal layout
        max_width = max((node.dimensions.x for node in nodes), default=0)
        xpos = self._last_x - (max_width + self._margin_x) if level != 0 else 0
        self._last_x = xpos

        # Layout Y positions (top-down)
        y = 0
        for node in nodes:
            node.location.y = y
            y -= node.dimensions.y + self._margin_y
            node.location.x = xpos

        # Recenter vertically
        y += self._margin_y  # last y goes one margin too far
        center = y / 2
        shift = center - self._average_y
        self._average_y = center

        for node in nodes:
            node.location.y -= shift

        # Restore parents
        for node, parent in zip(nodes, parents):
            node.parent = parent


if __name__ == '__main__':
    import bpy

    g = bpy.data.node_groups['Dual Lobe Specular']
    arranger = NodeTreeArranger(400, 600)
    arranger.arrange_nodes(g)
