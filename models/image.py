from .media import Media


class Image(Media):
    def __init__(self, path, descr, dimensions, print_where) -> None:
        super().__init__(path, descr)
        self.dimensions = dimensions
        self.print_where = print_where
