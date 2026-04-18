def open_or_senior(data):
    return ["Senior" if player[0] >= 55 and player[1] > 7 else "Open" for player in data]
if __name__ == '__main__':
    input = [[18, 20], [45, 2], [61, 12], [37, 6], [21, 21], [78, 9]]
    print(open_or_senior(input))