from node import Node as Node


class BinarySearchTree:
    root: Node = None
    inner_list = []

    def __str__(self):
        self.inner_list = []
        self._traverse(self.root)
        return str(self.inner_list)

    def find_node(self, data):
        tem_root: Node = self.root
        while True:
            if tem_root.data >= data:
                if tem_root.left is None:
                    return tem_root
                tem_root = tem_root.left
            else:
                if tem_root.right is None:
                    return tem_root
                tem_root = tem_root.right

    def add(self, data):
        if self.root is None:
            self.root = Node(data)
        else:
            node: Node = self.find_node(data=data)
            new_node = Node(data)
            if data <= node.data:
                node.left = new_node
            else:
                node.right = new_node

    def _traverse(self, current_node: Node):
        if current_node is None:
            return
        self._traverse(current_node.left)
        self.inner_list.append(current_node.data)
        self._traverse(current_node.right)

    def is_present(self, data):
        tem_root: Node = self.root
        previous_node = None
        while tem_root:
            if tem_root.data >= data:
                if tem_root.data == data:
                    return True, tem_root, previous_node
                previous_node = tem_root
                tem_root = tem_root.left
            else:
                if tem_root.data == data:
                    return True, tem_root, previous_node
                previous_node = tem_root
                tem_root = tem_root.right
        return False, None

    @staticmethod
    def is_leaf(node: Node):
        return node.left is None and node.right is None

    def delete(self, data):
        node_list = self.is_present(data)
        required_node = node_list[1]
        if self.is_leaf(required_node):
            if node_list[2].left.data == data:
                node_list[2].left = None
            elif node_list[2].right.data == data:
                node_list[2].right = None
        elif required_node.left is None and required_node.right is not None:
            required_node.data = required_node.right.data
            required_node.right = None
        elif required_node.right is None and required_node.left is not None:
            required_node.data = required_node.left.data
            required_node.left = None
        else:
            node = node_list[1]
            lit=bst.find_next_greater_from(node)
            node_to_move =lit[0]
            if node_to_move.right is not None:
                node.data = node_to_move.data
                node.right = node_to_move.right
            else:
                node.data = node_to_move.data
                lit[1].left = None

    @staticmethod
    def find_next_greater_from(node: Node):
        node = node.right
        previous_node = None
        while node.left is not None:
            previous_node = node
            node = node.left
        return node,previous_node


if __name__ == '__main__':
    bst = BinarySearchTree()
    values = [
        -1, 100, 200, 300, -400, -500, 600,
        45, -23, 999, 0, 17, -75, 350, 720,
        -1000, 88, 5, 250, -19
    ]

    for v in values:
        bst.add(v)

    print(bst)
    bst.delete(300)
    print(bst)
