import bcrypt


class Encrypt:
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(password: str, hash: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))
