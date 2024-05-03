""""
Password salting and hashing example
This is from James Eddy's Course
"""

import hashlib
import os  # << hint


def hash_pw(plain_text, salt='') -> str:
    """

    :param plain_text: str (user-supplied password)
    :param salt: str
    :return: str (ASCII-encoded salt + hash)
    """
        
    salt = os.urandom(20).hex()
    hashable = salt + plain_text  # concatenate salt and plain_text
    hashable = hashable.encode('utf-8')
    this_hash = hashlib.sha1(hashable).hexdigest()  # hash w/ SHA-1 and hexdigest
    return salt + this_hash  # prepend hash and return


def authenticate(stored, plain_text, salt_length=None) -> bool:
    """
    Authenticate by comparing stored and new hashes.

    :param stored: str (salt + hash retrieved from database)
    :param plain_text: str (user-supplied password)
    :param salt_length: int
    :return: bool
    """

    salt_length = 40  # set salt_length
    salt = stored[:salt_length]  # extract salt from stored value
    stored_hash = stored[salt_length:]  # extract hash from stored value
    hashable = salt + plain_text  # concatenate hash and plain text
    hashable = hashable.encode('utf-8')
    this_hash = hashlib.sha1(hashable).hexdigest()  # hash and digest
    # print("this hash", this_hash)
    # print("stored hash", stored_hash)
    return this_hash == stored_hash  # compare
    

def check_password(password: str):

    """
    pass_check ="^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    re.match(pre_check, password)
    """
    spec_char = ['@', '#', '$', '%', '!', '?', '&', '*', '(', ')', '-', '_', '+', '=']
    if len(password) >= 8 and len(password) <= 25:
        # check character and number
        upper = False
        lower = False
        special_char = False
        number = False
        for p in password:
            if p.isupper():
                upper = True
            elif p.islower():
                lower = True
            elif p.isnumeric():
                number = True
            elif p in spec_char:
                special_char = True
        if upper and lower and special_char and number:
            return True
        return False
    else:
        print("incorrect password length")
        return False