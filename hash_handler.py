import hashlib
import secrets


def gen_salt():
    """
    Produces a randomly generated and URL safe string (16 chars) and returns it.

    Returns:
        str: A random and URL safe string of 16 chars.
    """
    
    return secrets.token_urlsafe(16)


def get_global_pepper():
    """
    Produces a predetermined URL safe string (32 chars) and returns it.

    Returns:
        str: An URL safe string of 32 chars.
    """
    
    # i manually generated the pepper using secrets.token_urlsafe(32), and hard coded as a constant string saved in this function
    return "Jz9QMZRTFZ3XhH0JOmpF3Ntp1C_Eg98rgad3DMn8tBw"


def hash_password(text: str):
    """
    Hashes a given string in SHA256 and return the product in hexadecimal format.

    Args:
        text (str): A text that is to be hashed (like a password).

    Returns:
        str: the hashed password in hexadecimal format.
    """
    
    # use SHA256 to hash the text (in this code it will be mostly passwords), then return the hexadecimal of the hash value
    hash_object = hashlib.new("SHA256")
    hash_object.update(text.encode())
    password_hash = hash_object.hexdigest()
    
    return str(password_hash)
