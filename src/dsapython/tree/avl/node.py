class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
        self.height = 1

    def __repr__(self):
        return (f"Node(data={self.data!r}, "
                f"left={self.left!r}, "
                f"right={self.right!r},"
                f"height={self.height})")
