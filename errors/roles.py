class RoleNotFound(Exception):
    def __init__(self, role_id: int):
        self.role_id = role_id
        super().__init__(f"Role '{role_id}' not found")


class RoleAlreadyExists(Exception):
    def __init__(self, role_id: int):
        self.role_id = role_id
        super().__init__(f"Role '{role_id}' already exists")
