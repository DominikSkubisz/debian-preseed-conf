#!/usr/bin/env python3
import getpass
from passlib.hash import sha512_crypt


if __name__ == "__main__":
    pwd = getpass.getpass("Password:")
    pwd_rep = getpass.getpass("Retype password:")
    if pwd == pwd_rep:
        print(sha512_crypt.hash(pwd))
    else:
        print("Passwords do not match")
