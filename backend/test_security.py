from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)

password = "123456"

print("Password:", password)

hashed = hash_password(password)

print("\nHash:")
print(hashed)

print("\nVerify:")

print(
    verify_password(
        password,
        hashed,
    )
)

token = create_access_token(
    {
        "sub": "1",
        "email": "adeesha@example.com",
    }
)

print("\nJWT:")
print(token)

print("\nDecoded:")

print(
    decode_access_token(token)
)