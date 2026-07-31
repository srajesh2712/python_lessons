class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        #return len(self.items) == 0
        return not self.items
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()
    def peek(self):
        return self.items[-1]
    def size(self):
        return len(self.items)
    def __str__(self):
        return str(self.items)

def reverse_string_fast(my_string):
    # Use the "accumulator pattern."
    # Start with an "empty bucket" of the right data type,
    # and build the solution by filling the bucket within a loop.
    reversed_string = ""

    # Create a new stack
    s = Stack()
    # Iterate through my_string and push the characters onto the stack
    for char in my_string:
        s.push(char)
    # Use a while loop with the exit condition that the stack is empty.
    # Within this loop, update reversed_string with characters popped off the stack.
    accumulator = []
    while not s.is_empty():
        #reversed_string += s.pop()
        accumulator.append(s.pop())
    # Return the result
    #return reversed_string
    return "".join(accumulator)

def reverse_string_slow(my_string):
    # Use the "accumulator pattern."
    # Start with an "empty bucket" of the right data type,
    # and build the solution by filling the bucket within a loop.
    reversed_string = ""

    # Create a new stack
    s = Stack()
    # Iterate through my_string and push the characters onto the stack
    for char in my_string:
        s.push(char)
    # Use a while loop with the exit condition that the stack is empty.
    # Within this loop, update reversed_string with characters popped off the stack.

    while not s.is_empty():
        reversed_string += s.pop()

    # Return the result
    return reversed_string



if __name__ == "__main__":
    s = Stack()
    print(s)
    print(s.is_empty())
    s.push(1)
    s.push("Rajesh")
    print(s)
    print(s.pop())
    print(s.peek())
    print(s.size())

    test_string = "gninraeL nIdekniL htiw tol a nraeL"
    result = reverse_string_fast(test_string)
    print(result)