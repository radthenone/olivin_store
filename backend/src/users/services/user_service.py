class UserService:
    def __init__(self, repository, *args, **kwargs):
        self.user_repository = repository
        super().__init__(*args, **kwargs)
