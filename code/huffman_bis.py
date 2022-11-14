# Huffman Compression
from heapq import heapify, heappop, heappush
class Node:
    def __init__(self, freq, ch, left=None, right=None):
        self.freq = freq
        self.ch = ch
        self.left = left
        self.right = right
    def __lt__(self, other):
        return self.freq < other.freq
    def __gt__(self, other):
        return self.freq > other.freq
    def __add__(self, other):
        return self.freq + other.freq   


class Huffman:
    def __init__(self, list):
        self.list = list
        self.tree = Huffman.huffTree(self, list)
    def huffTree(self, list):
        if len(self.list) == 0:
            return None
        fq = {ch: self.list.count(ch) for ch in set(self.list)}
        heap = [Node(fq, ch) for (ch, fq) in fq.items()]
        heapify(heap)
        while len(heap) >= 2:
            cp1 = heappop(heap)
            cp2 = heappop(heap)
            heappush(heap, Node((cp1 + cp2), None, cp1, cp2))
        return heappop(heap)
    def encode(self, prefix, code, side=None):
        for i in self.list:
            if self.tree.ch == i:
                code[prefix] = i
            elif i == self.tree.right:
                code[prefix + '1'] = i
            elif i == self.tree.left:
                code[prefix + '0'] = i
            else:
                Huffman.encode(self, prefix + '1', code, 'right')
                Huffman.encode(self, prefix + '0', code, 'left')
        return code
        if self.tree.ch is not None:
            code[prefix + self.tree.ch]
        else:
            for i in self.list
        




