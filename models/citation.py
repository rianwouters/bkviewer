from .array import Array

class Citation:
    def __init__(self, descr, type, text=None, info=None):
        self.descr = descr
        self.text = text
        self.info = info
        self.files = Array('Files')
