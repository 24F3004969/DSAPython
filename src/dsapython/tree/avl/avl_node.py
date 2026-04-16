class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
        self.height = 0

    def __repr__(self):
        return f"Node(data={self.data}, height={self.height})"
