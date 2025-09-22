class ApiError:
    def __init__(self, status: str, code: str, title: str, detail: str):
        self.status = status
        self.code = code
        self.title = title
        self.detail = detail