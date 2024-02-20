import bcrypt
from fastapi import HTTPException
from jose import jwt
from configuration.config import Settings

def hash_password(password: str) -> str:
    # Hash the password with a randomly generated salt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def check_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )
SECRET_KEY: str = "2znmyRG!&)oloEKphqFQQ@6{]Q7T&W4S79GAbdqvNX{U2!3ZqR;Rv!:^G}@D-=O)"

def decode_bearer_token(token: str) -> dict:
    try:
        # Decode the token using the provided secret key
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
#

# password = "1234"

# hashedpassword = hash_password(password)
# print(f"Hashed Password {password} is {hashedpassword}")


# if check_password(
#     "123", "$2b$12$Fm3D3PMGRxWy./1ZihopoOonkZx.83E48xV7qWpTTPAW0bgLs3R5u"
# ):
#     print("Password is correct!")
# else:
#     print("Incorrect password.")

import secrets
import string
def generate_random_key(length=64):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?/~"
    return "".join(secrets.choice(alphabet) for _ in range(length))
# # Generate a random key
# random_key = generate_random_key()
# print("Randomly Generated Key:", random_key)
