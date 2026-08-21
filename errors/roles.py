class RoleNotFound(Exception):
    def __init__(self, role_id: int):
        self.role_id = role_id
        super().__init__(f"Role '{role_id}' not found")


class RoleAlreadyExists(Exception):
    def __init__(self, code: str):
        self.code = code
        super().__init__(f"Role '{code}' already exists")
