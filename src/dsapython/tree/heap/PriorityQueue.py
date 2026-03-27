class PriorityQueue:
    def __init__(self):
        self.heap = []

    # Index helpers
    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    # Insert (priority, value)
    def insert(self, priority, value):
        self.heap.append((priority, value))
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, i):
        while i > 0 and self.heap[i][0] < self.heap[self._parent(i)][0]:
            self._swap(i, self._parent(i))
            i = self._parent(i)

    # Delete element with highest priority (min priority value)
    def delete(self):
        if not self.heap:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def _heapify_down(self, i):
        smallest = i
        left = self._left(i)
        right = self._right(i)

        if left < len(self.heap) and self.heap[left][0] < self.heap[smallest][0]:
            smallest = left

        if right < len(self.heap) and self.heap[right][0] < self.heap[smallest][0]:
            smallest = right

        if smallest != i:
            self._swap(i, smallest)
            self._heapify_down(smallest)