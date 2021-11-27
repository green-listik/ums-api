import bcrypt


def verify_password(password: str, hashed_password):
    pwhash = bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    return pwhash
