class Node:
    def __init__(self, data, left=None, right=None, parent=None):
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent
        self.height = 1  # Standard for new AVL nodes

    def __repr__(self):
        return f"Node(data={self.data}, height={self.height})"
