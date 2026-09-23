class InvalidRequest(Exception):
    """Demande de simulation rejetée : l'API la traduit en réponse 400 (R-06)."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
