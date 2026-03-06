class SuperAdminUser:
    def __init__(self, role="super_admin"):
        self.role = role
        self.id = None  # optional if you use user ID in caching

    @property
    def is_authenticated(self):
        return True
