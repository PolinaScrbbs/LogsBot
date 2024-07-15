import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy import String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

from ...config import SECRET_KEY

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(1024), nullable=False)
    # name: Mapped[str] = mapped_column(String(64), nullable=False)
    # surname: Mapped[str] = mapped_column(String(64), nullable=False)
    # patronymic: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(40), unique=True, nullable=True)
    # phone_number: Mapped[str] = mapped_column(CHAR(15), unique=True, nullable=True)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    mailing_consent: Mapped[bool] = mapped_column(default=False, nullable=False)

    def set_password(self, password: str) -> None:
        self.hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))
    
    def generate_token(self, expires_in: int = 3600) -> str:
        payload = {
            "user_id": self.id,
            "exp": datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    @staticmethod
    def verify_token(token: str) -> int:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload["user_id"]
        except jwt.ExpiredSignatureError:
            raise Exception("Токен истек")
        except jwt.InvalidTokenError:
            raise Exception("Неверный токен")

