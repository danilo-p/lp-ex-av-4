NULL = -1  # The null link


class HeapManager:
    """ Implements a very simple heap manager ."""

    def __init__(self, initialMemory):
        """ Constructor. Parameter initialMemory is the array of
            data that we will use to represent the memory."""
        self.memory = initialMemory
        self.memory[0] = self.memory.__len__()
        self.memory[1] = NULL
        self.freeStart = 0

    def allocate(self, requestSize):
        """ Allocates a block of data, and return its address. The
            parameter requestSize is the amount of space that must be allocated."""
        size = requestSize + 1
        # Do first-fit search: linear search of the free list for the first block
        # of sufficient size.
        p = self.freeStart
        lag = NULL
        while p != NULL and self.memory[p] < size:
            lag = p
            p = self.memory[p + 1]
        if p == NULL:
            raise MemoryError()
        nextFree = self.memory[p + 1]
        # Now p is the index of a block of sufficient size ,
        # lag is the index of p’s predecessor in the
        # free list , or NULL , and nextFree is the index of
        # p’s successor in the free list , or NULL .
        # If the block has more space than we need , carve
        # out what we need from the front and return the
        # unused end part to the free list .
        unused = self.memory[p] - size
        if unused > 1:
            nextFree = p + size
            self.memory[nextFree] = unused
            self.memory[nextFree + 1] = self.memory[p + 1]
            self.memory[p] = size
        if lag == NULL:
            self.freeStart = nextFree
        else:
            self.memory[lag + 1] = nextFree
        return p + 1

    def deallocate(self, blockAddress):
        """ Deallocates a block of data. The parameter blockAddress the address
            of the block that must be deallocated."""
        blockStart = blockAddress - 1

        if blockStart < self.freeStart:
            # In this case, the block is before the head of the free block
            # list. We need to turn it into the head of the free block list and
            # change the next free pointer to be the old head.
            self.memory[blockStart + 1] = self.freeStart
            self.freeStart = blockStart
        else:
            # In this case, the block is after the head of the free block list,
            # so we need insert this block in the middle of the free block list.
            # To do so, we need to search for the free block that is right
            # before the one we want to deallocate. After finding the previous
            # block, we need to point the block's next free pointer to the one
            # that the previous was pointing to, and then point the previous to the
            # block we want to deallocate.

            # Linear search of the free list for the block that comes before the
            # one we are trying to deallocate.
            currFreeBlock = self.freeStart
            prevFreeBlock = NULL
            while currFreeBlock != NULL and currFreeBlock < blockStart:
                prevFreeBlock = currFreeBlock
                currFreeBlock = self.memory[currFreeBlock + 1]
            if currFreeBlock == NULL:
                raise MemoryError()

            # Add reference to the next free block that the previous was pointing to.
            self.memory[blockStart + 1] = self.memory[prevFreeBlock + 1]

            # Point the previous block to the one we want to deallocate.
            self.memory[prevFreeBlock + 1] = blockStart


def test():
    h = HeapManager([0 for x in range(0, 15)])

    print("initial state", ", Memory = ",
          h.memory, ", freeStart = ", h.freeStart)

    a = h.allocate(2)
    print("a = ", a, ", Memory = ", h.memory, ", freeStart = ", h.freeStart)

    b = h.allocate(2)
    print("b = ", b, ", Memory = ", h.memory, ", freeStart = ", h.freeStart)

    c = h.allocate(2)
    print("c = ", c, ", Memory = ", h.memory, ", freeStart = ", h.freeStart)

    h.deallocate(a)
    print("a deallocated", ", Memory = ",
          h.memory, ", freeStart = ", h.freeStart)

    h.deallocate(b)
    print("b deallocated", ", Memory = ",
          h.memory, ", freeStart = ", h.freeStart)

    h.deallocate(c)
    print("c deallocated", ", Memory = ",
          h.memory, ", freeStart = ", h.freeStart)

test()
