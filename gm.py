class A:
    def __init__(self) -> None:
        self.a = "A"

class B(A):
    def __init__(self) -> None:
        self.b = "B"


def main():
    b = B()
    print(b.a)


if __name__ == "__main__":
    main()
