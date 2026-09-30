from pwdlib import PasswordHash

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


password_hash = PasswordHash.recommended()


def normalize_email(
    email: str
) -> str:

    return email.strip().lower()


def register_user(
    db: Session,
    name: str,
    email: str,
    password: str
) -> User:

    email = normalize_email(email)

    existing_user = db.scalar(
        select(User).where(
            User.email == email
        )
    )

    if existing_user:

        raise ValueError(
            "An account with this email already exists."
        )

    user = User(
        name=name.strip(),
        email=email,
        password_hash=password_hash.hash(
            password
        )
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return user


def authenticate(
    db: Session,
    email: str,
    password: str
) -> User | None:

    email = normalize_email(email)

    user = db.scalar(
        select(User).where(
            User.email == email
        )
    )

    if not user:
        return None

    if not password_hash.verify(
        password,
        user.password_hash
    ):
        return None

    return user