import sys


def reverse_words(text):

    words =text.split(" ")
    rev =[word[::-1] for word in words ]

    return " ".join(rev)


if __name__ == '__main__':
    print(reverse_words("This is an example!" ))
    print(reverse_words("double  spaces"))
