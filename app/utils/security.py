import datetime
import calendar
import jwt
import base64
import hashlib
import hmac

class Security:
    PWD_HASH_SALT = b'SomeMegaSecretWow_VADIM_PRIVET'
    PWD_HASH_ITERATIONS = 101_010
    PWD_ALGORITHM = 'sha256'

    JWT_SECRET = 'ThisIsJWTSecret'
    JWT_ALGORITHM = 'HS256'

    def generate_access_token(self, **data):
        """Генерирует 30 минутый токен """
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())

        return jwt.encode(data, self.JWT_SECRET, algorithm=self.JWT_ALGORITHM)

    def generate_refresh_token(self, **data):
        """Генерирует 30 дневный refresh-токен"""
        days30 = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        data["exp"] = calendar.timegm(days30.timetuple())

        return jwt.encode(data, self.JWT_SECRET, algorithm=self.JWT_ALGORITHM)

    def generate_tokens(self, **data):
        """Генерирует access и refresh токены и возращает словарем"""
        access_token = self.generate_access_token(**data)
        refresh_token = self.generate_refresh_token(**data)
        return {"access_token": access_token,
                "refresh_token": refresh_token}

    def decode_token(self, token):
        """Декодирует токен"""
        return jwt.decode(token, self.JWT_SECRET, self.JWT_ALGORITHM)

    def check_token(self, token):
        """Возвращает True если токен декодирован и валиден"""
        try:
            jwt.decode(token, self.JWT_SECRET, algorithms=[self.JWT_ALGORITHM])
            return True
        except Exception as e:
            print(e)
            return False

    def get_hash(self, password):
        """Возвращает закодированный хещ-пароль из простого пароля-строли"""
        x = hashlib.pbkdf2_hmac(
            self.PWD_ALGORITHM,
            password.encode('utf-8'),  # Convert the password to bytes
            self.PWD_HASH_SALT,
            self.PWD_HASH_ITERATIONS
        )
        return base64.b64encode(x)

    @staticmethod
    def is_passwords_equals(first_password, second_password):
        """Сравнивает два закодированных хеш-пароля"""
        first_password = base64.b64decode(first_password)
        second_password = base64.b64decode(second_password)
        return hmac.compare_digest(first_password, second_password)