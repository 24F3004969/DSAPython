from dsapython.tree.avl.node import Node


class AVLBinaryTreeClass:
    root: Node = None
    inner_list = []

    @staticmethod
    def height(node) -> int:
        if node is None:
            return 0
        return node.height

    def get_balance_factor(self, node):
        if node is None:
            return 0
        return self.height(node.left) - self.height(node.right)

    def rotate_left(self, node: Node):

        pass

    def rotate_right(self, node: Node):
        pass

    def insert(self, value):
        pass

    def delete(self, value):
        pass

    def search(self, value):
        pass
