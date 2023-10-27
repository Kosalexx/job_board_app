class FileMock:
    def __init__(self, size: int | None = None, name: str | None = None) -> None:
        self._size = size
        self._name = name

    @property
    def size(self) -> int | None:
        return self._size

    @property
    def name(self) -> str | None:
        return self._name
