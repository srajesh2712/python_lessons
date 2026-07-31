from collections import deque
class Queue:
    def __init__(self):
        self.items = deque()

    def is_empty(self):
        return not self.items
    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.popleft()

    def size(self):
        return len(self.items)

    def peek(self):
        return self.items[0]

    def __str__(self):
        return str(self.items)

def queue_challenge():
    my_queue = Queue()
    word_list =  ["wore", "a", "silly", "hat", "the", "aardvark"]
    for word in word_list:
        my_queue.enqueue(word)

    my_queue.enqueue(my_queue.dequeue())
    my_queue.enqueue(my_queue.dequeue())
    my_queue.enqueue(my_queue.dequeue())
    my_queue.enqueue(my_queue.dequeue())
    my_queue.enqueue(my_queue.dequeue())
    return my_queue.items

if __name__ == '__main__':
    result = queue_challenge()
    print(result)