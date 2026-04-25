def likes(names):
    n = len(names)
    formats = {
        0: "no one likes this",
        1: "{} likes this",
        2: "{} and {} like this",
        3: "{}, {} and {} like this",
        4: "{}, {} and {others} others like this"
    }
    template = formats[min(n, 4)]
    if n < 4:
        return template.format(*names)
    return template.format(names[0], names[1], others=n - 2)

if __name__ == '__main__':
    print(likes(["Alex", "Jacob", "Mark", "Max"] ))