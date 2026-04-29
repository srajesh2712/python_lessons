class Deck:
    def __init__(self):
        self.cards = [f'{rank}-{suit}' for suit in ['spade','heart'] for rank in range(4)]
    def __len__(self):
        return len(self.cards)
    def __getitem__(self, index):
        return self.cards[index]
deck = Deck()
print(deck.cards)

for card in deck.cards:
    print(card)

print(len(deck))
print(deck[1])


class Incrementer:
    def __init__(self,step):
        self.step = step
        self.count = 0
    def __call__(self):
        self.count += self.step
        return self.count

inc_by_2 = Incrementer(2)
print(inc_by_2())
print(inc_by_2())



class ReadOnlyAccount:
    def __init__(self,dict):
        super().__setattr__('_dict', dict)
    def __getattr__(self, item):
        try:
            return self._dict[item]
        except KeyError:
            raise AttributeError(' no such attribute')
    def __setattr__(self, key, value):
        self._dict[key] = value
readonly = ReadOnlyAccount({'name':'Rajesh','age':'40'})


readonly.course='Bigdata'
print(readonly.course)