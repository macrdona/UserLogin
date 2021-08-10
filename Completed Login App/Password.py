import re

class Password:

    def __init__(self):
        None
    
    #This method ensure that the password follows the requirements
    def validatePassword(self, password):
        self.password = password
        valid = 0
        if len(self.password) < 8:
            valid = -1
        elif not re.search("[a-z]", self.password):
            valid = -1
        elif not re.search("[A-Z]", self.password):
            valid = -1
        elif not re.search("[0-9]", self.password):
            valid = -1
        elif not re.search("[_@$]", self.password):
            valid = -1
        elif re.search("\s", self.password):
            valid = -1

        return valid