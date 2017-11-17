
class Client(object):
    clientId = None
    assetUrl = None
    ipaFolder = None
    zipFile = None

    def __init__(self, clientId, assetUrl, ipaFolder):
        self.clientId = clientId
        self.assetUrl = assetUrl
        self.ipaFolder = ipaFolder
    
    def load(self):
        with open(self.clientId, "r") as ins:
            array = []
            for line in ins:
                array.append(line)
            return array
        

    def release():
        print('release')