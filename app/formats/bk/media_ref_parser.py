from .file_ref_parser import FileRefParser
from models import MediaRef


class MediaRefParser(FileRefParser):
    def handle(self, r, n, ref):
        media = MediaRef(r['path'], r['descr'])
        ref.media[n-1] = media
        return media