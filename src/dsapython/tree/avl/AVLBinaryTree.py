from dsapython.tree.avl.avl_node import Node


class AVLBinaryTreeClass:
    root: Node = None
    inner_list = []
    orin: str = ''

    def __str__(self):
        self.inner_list = []
        self._traverse(self.root)
        return str(self.inner_list)

    @staticmethod
    def get_height(node: 'Node') -> int:
        if node is None:
            return 0
        return node.height

    def update_height(self, node: Node):
        node.height = 1 + max(self.get_height(node.left),
                              self.get_height(node.right))

    def _traverse(self, current_node: Node):
        if current_node is None:
            return
        self._traverse(current_node.left)
        self.inner_list.append(current_node.data)
        self._traverse(current_node.right)

    def get_balance_factor(self, node):
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def insert(self, data):
        self.orin = ''
        self.root = self.insert_recursive(node=self.root, data=data)

    def insert_recursive(self, node, data):
        if node is None:
            return Node(data)

        if data <= node.data:
            self.orin += 'L'
            node.left = self.insert_recursive(node.left, data)
            node = self.balance_tree(node, 'L')
        else:
            self.orin += 'R'
            node.right = self.insert_recursive(node.right, data)
            node = self.balance_tree(node, 'R')
        return node

    def balance_tree(self, start: Node, ir):
        self.update_height(start)
        balance_factor = self.get_balance_factor(start)
        print(balance_factor, start, self.orin, start.data)
        if balance_factor == 1 or balance_factor == -1 or balance_factor == 0:
            return start
        elif balance_factor > 0:
            print(self.orin, "right rotate")
            # correct the orientation
            if self.orin[-1] == 'R' and ir == 'L':
                return self.rotate_left_right(start)
            return self.rotate_right(start)
        elif balance_factor < 0:
            print(self.orin, "left rotate")
            # correct the orientation
            if self.orin[-1] == 'L' and ir == 'R':
                return self.rotate_right_left(start)
            return self.rotate_left(start)
        return None

    # def find_node(self, data, tem_root: Node) -> Node:
    #     if tem_root.data >= data:
    #         if tem_root.left is None:
    #             return tem_root
    #         return self.find_node(data, tem_root.left)
    #     else:
    #         if tem_root.right is None:
    #             return tem_root
    #         return self.find_node(data, tem_root.right)

    def delete(self, value):
        pass

    def search(self, value):
        pass


    def rotate_left(self,node: Node):
        right_node = node.right
        left_node_right = right_node.left
        node.right = left_node_right
        right_node.left = node
        self.update_height(node)
        self.update_height(right_node)
        return right_node

    def rotate_left_right(self, node: Node):
        # Step 1: Perform a Left Rotation on the left child
        node.left = self.rotate_left(node.left)

        # Step 2: Perform a Right Rotation on the parent node
        return self.rotate_right(node)

    def rotate_right(self,node: Node):
        left_node = node.left
        right_node_left = left_node.right
        node.left = right_node_left
        left_node.right = node
        self.update_height(node)
        self.update_height(left_node)
        return left_node

    def rotate_right_left(self, node: Node):
        node.right = self.rotate_right(node.right)
        return self.rotate_left(node)
