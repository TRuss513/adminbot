    
''' Exception class to call whenever any authentication error occurs '''
class authenticationError(Exception):
    def __init__(self, errorMsg):
        self.errorMsg = errorMsg
        
    def __str__(self):
        return repr(self.errorMsg)