import random
class CAESER_SHIFT():
    def __init__(self):
        pass
    def encryptString(self,string):
        encryptedString = ""
        for letter in string:
            encryptedString += chr((ord(letter) + 346))
        return encryptedString
    def decryptString(self,string):
        decryptedString = ""
        for letter in string:
            decryptedString += chr((ord(letter) - 346 ))
        return decryptedString
    
        


