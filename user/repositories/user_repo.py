
from common.repository.base_repository import BaseRepository
from user.models.user_model import User


class UserRepository(BaseRepository):
    def __init__(self):
        self.model = User
