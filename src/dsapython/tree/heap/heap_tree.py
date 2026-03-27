def _parent(index):
    return (index - 1) // 2


def _left(index):
    return 2 * index + 1


def _right(index):
    return 2 * index + 2


class MinHeap:
    def __init__(self):
        self.heap = []

    # Helper methods

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    # Insert an element into the heap
    def insert(self, value):
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, index):
        while index > 0 and self.heap[index] < self.heap[_parent(index)]:
            self._swap(index, _parent(index))
            index = _parent(index)

    # Delete (extract) the minimum element
    def delete(self):
        if not self.heap:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)

        return root

    def _heapify_down(self, index):
        smallest = index
        left = _left(index)
        right = _right(index)

        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right

        if smallest != index:
            self._swap(index, smallest)
            self._heapify_down(smallest)

    # Optional: view heap
    def __str__(self):
        return str(self.heap)
