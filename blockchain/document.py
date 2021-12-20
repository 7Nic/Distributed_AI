import pathlib

class Document:
    def __init__(self, title: str, body: str):
        """
        Classe que define um documento de texto.

        Args
            title (str): título do documento.
            body (str): corpo do texto.
        """
        self._title = title
        self._body = body
    
    @classmethod
    def document_from_file(cls, filepath: pathlib.Path):
        return cls(filepath.name, filepath.read_text())

    def __eq__(self, other) -> bool:
        if isinstance(other, Document):
            return self._title == other._title and self._body == other._body
        return False

    @property
    def title(self):
        return self._title
    
    @property
    def body(self):
        return self._body