class Fila(list):

    def __init__(self, lista):
        super().__init__(item for item in lista)

    def push(self, x):
        super().append(x)

    def pop(self):
        return super().pop(0)

    def __repr__(self):
        return f"Fila -> {super().__repr__()}"


def main():
    f = Fila([1,2,3,4,5,6])
    print(f)
    f.push(8)
    print(f)
    f.pop()
    f.pop()
    print(f)


if __name__ == "__main__":
    main()

