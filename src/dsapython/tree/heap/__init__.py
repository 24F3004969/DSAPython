from dsapython.tree.heap.heap_tree import MinHeap

heap = MinHeap()

heap.insert(10)
heap.insert(5)
heap.insert(20)
heap.insert(2)

print(heap)          # [2, 5, 20, 10]
print(heap.delete()) # 2
print(heap.delete()) # 5
print(heap)          # [10, 20]