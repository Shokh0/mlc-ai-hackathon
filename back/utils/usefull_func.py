import hashlib

def hashPassword(password):
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256()
    hash_object.update(password_bytes)
    hashed_password = hash_object.hexdigest()
    return hashed_password
