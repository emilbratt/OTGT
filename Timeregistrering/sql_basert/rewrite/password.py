import hashlib,os,binascii
from visual import getUserValue


# returns password hash
def passwordStore(pwd):
    # pwd = getUserValue(1,'skriv inn nytt passord')

    pwd = str(pwd[0][0])
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdHash = hashlib.pbkdf2_hmac('sha256',pwd.encode(
                                    'utf-8'), salt, 100)

    pwdHash = binascii.hexlify(pwdHash)
    L = []
    L.append((salt + pwdHash).decode('ascii'))
    L = tuple(L)
    LT = []
    LT.append(L)
    # return pwdHash
    return L


# returns true if password hash and password input matches
def passwordVerify(pwdStored, pwd):
    salt = pwdStored[:64]
    pwdStored = pwdStored[64:]

    pwdHash = hashlib.pbkdf2_hmac('sha256', pwd.encode(
                    'utf-8'), salt.encode('ascii'), 100)

    pwdHash = binascii.hexlify(pwdHash).decode('ascii')
    return pwdHash == pwdStored
