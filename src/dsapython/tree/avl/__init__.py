from dsapython.tree.avl import AVLBinaryTree

avl_tree = AVLBinaryTree.AVLBinaryTreeClass()
li = [-1, 100, 200, 300, -400, -500, 600,
      45, -23, 999, 0, 17, -75, 350, 720,
      -1000, 88, 5, 250, -19]
for i in li:
    avl_tree.insert(i)
print(avl_tree)
