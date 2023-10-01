#!/usr/bin/env python3
import getpass
from passlib.hash import sha512_crypt


def mkhash(password):
    if password == '':
        return ''
    else:
        return sha512_crypt.hash(password)


if __name__ == "__main__":
    pwd = getpass.getpass("Password:")
    pwd_rep = getpass.getpass("Retype password:")
    if pwd == pwd_rep:
        print(mkhash(pwd))
    else:
        print("Passwords do not match")
