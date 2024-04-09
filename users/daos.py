from users.models import CustomUser


class CustomUserDAO:
    __slots__ = ('_db',)

    def __init__(self):
        self._db = CustomUser

    def get(self, user_id: int):
        return self._db.objects.get(id=user_id)

