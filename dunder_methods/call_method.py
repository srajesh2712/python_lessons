class Calculator:
    def __init__(self):
        self._cache = {}
    def __call__(self, x):
        if x in self._cache:
            print(' returning cached ')
            return self._cache[x]
        print(' calculating x ')
        result = x * x
        self._cache[x] = result
        return result
calc = Calculator()
print( calc(4))