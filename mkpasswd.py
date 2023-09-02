#!/usr/bin/env python3
import os
import sys
import crypt
import getpass

if __name__ == "__main__":
    pwd = str(getpass.getpass("Password:"))
    pwd2 = str(getpass.getpass("Retype password:"))
    if pwd == pwd2:
        print(crypt.crypt(pwd, crypt.mksalt(crypt.METHOD_SHA512)))
    else:
        print("Passwords not match")
