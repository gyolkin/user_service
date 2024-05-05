from user_service.application.protocols.password_manager import PasswordManager


class FakePasswordManager(PasswordManager):
    def hash_password(self, password: str) -> str:
        return f'hashed-{password}'

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return hashed_password == self.hash_password(password)
