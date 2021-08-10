import hashlib

#creating class hash
class Hash:
    #contructor to initialize password
    def __init__(self, password):
        self.password = password
        
    #return the hash value of the given password
    '''After the password has been hashed, it is then converted into hexadecimal form.
        It returns as a string that can be store into the database'''
    def hashFunction(self, salt):
        result = hashlib.pbkdf2_hmac('sha256',self.password.encode('utf-8'), salt, 100000).hex()
        return result

    