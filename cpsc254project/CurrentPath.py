# This function just holds the current path of the selected file
# This path will be used when the Encrypt/Decrypt buttons are pressed
#

class CurrentPath:
    _currentFilePath = None
    
    @classmethod
    def setFilePath(cls, file_path):
        cls._currentFilePath = file_path
        print(f"Current file path stored: {cls._currentFilePath}")
        
    @classmethod
    def getFilePath(cls):
        return cls._currentFilePath