class Pilha(list):

    def __init__(self, lista):
        super().__init__(item for item in lista)

    def push(self, x):
        super().append(x)

    def pop(self):
        return super().pop(-1)

    def __repr__(self):
        return f"Pilha -> {super().__repr__()}"


def main():
    f = Pilha([1,2,3,4,5,6])
    print(f)
    f.push(8)
    print(f)
    f.pop()
    print(f)
    f.pop()
    print(f)


if __name__ == "__main__":
    main()

