class ApiKeyNotFoundError(Exception):
    def __init__(self, message="API key not found"):
        self.message = message
        super().__init__(self.message)

    