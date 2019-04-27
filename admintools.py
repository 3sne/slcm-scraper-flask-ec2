import csv
import os
import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class DataPrepUtil:

    def __init__(self, dataRoot, **kwargs):
        self.dataRoot = dataRoot + os.sep
        self.listRegistrationNumberAndPasswords = []
        self.fileList = []
        self.passList = []
        self.fileAppender = '_profile_data.csv'
        # self.loadPublicKey()
        for key, val in kwargs.items():
            if key == 'auto' and val == 1:
                self.generatePassList()
            if key == 'searchfor':
                self.fileAppender = val

    def loadPublicKey(self):
        with open("keystore/af_public_key.pem", "rb") as key_file:
            self.af_public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())

    def generatePassList(self):
        self.updateFileList()
        self.passExtractor()
        self.saveLocally()

    def updateFileList(self):
        self.fileList.clear
        for subdir, dirs, files in os.walk(self.dataRoot):
            for file in files:
                regNo = subdir[len(self.dataRoot):]
                filepath = subdir + os.sep + file
                if file == regNo + self.fileAppender:
                    self.fileList.append(filepath)

    def passExtractor(self):
        for file in self.fileList:
            with open(file, 'r') as f:
                cReader = csv.DictReader(f)
                for row in cReader:
                    regNo = row['ApplicationNumber']
                    # enc_regNo = self.af_public_key.encrypt(regNo.encode(), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
                    pw = row['Password']
                    # enc_pw = self.af_public_key.encrypt(pw.encode(), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
                    lilDict = {
                        "username" : regNo,
                        "password": pw
                    }
                    self.passList.append(lilDict)

    def saveLocally(self):
        dflu = DataFileLocalUtil(self.passList)
        dflu.doIt()

    def getJsonifiedPassList(self):
        return json.dumps(self.passList)

class DataFileLocalUtil:
    
    def __init__(self, passList):
        self.passList = passList
        self.pftPath = 'pft'
        self.fOut = 'grid.csv'

    def doIt(self):
        self.ensurePftExists()
        with open(self.pftPath + os.sep + self.fOut, 'w') as f:
            cWriter = csv.DictWriter(f, fieldnames=['username', 'password'])
            cWriter.writeheader()
            for elem in self.passList:
                cWriter.writerow(elem)

    def ensurePftExists(self):
        if os.path.isdir(self.pftPath) == False:
            os.mkdir(self.pftPath)

if __name__ == '__main__':
    dpu = DataPrepUtil('./html', auto=1)
    print(dpu.fileList)
    print(dpu.getJsonifiedPassList())