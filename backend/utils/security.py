from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plaintext password against its hash."""
    return pwd_context.verify(plain, hashed)


def get_password_hash(password: str) -> str:
    """Hash a plaintext password."""
    return pwd_context.hash(password)


if __name__ == "__main__":
    hashed_password = get_password_hash("password")
    print(f"This is 'password' hashed: {hashed_password}")
    if verify_password("password", hashed_password):
        print("Success!")
    else:
        print('Fail')