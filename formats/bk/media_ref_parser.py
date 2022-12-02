from .file_ref_parser import FileRefParser
from models import Media


class MediaRefParser(FileRefParser):
    def handle(self, r, n, ref):
        media = Media(r['path'], r['descr'])
        ref.media[n-1] = media
        return media