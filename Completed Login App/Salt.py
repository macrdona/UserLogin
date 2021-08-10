import os

class Salt:
    #This method provides a randomly computed salt
    def saltingFunction(self):
        salt = os.urandom(64)
        return salt