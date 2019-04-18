import csv
import os
import json

class DataPrepUtil:

    def __init__(self, dataRoot, **kwargs):
        self.dataRoot = dataRoot + os.sep
        self.listRegistrationNumberAndPasswords = []
        self.fileList = []
        self.passList = []
        self.fileAppender = 'ProfileData.csv'
        for key, val in kwargs.items():
            if key == 'auto' and val == 1:
                self.generatePassList()
            if key == 'searchfor':
                self.fileAppender = val

    def generatePassList(self):
        self.updateFileList()
        self.passExtractor()

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
                    pw = row['Password']
                    lilDict = {
                        "username" : regNo,
                        "password": pw
                    }
                    self.passList.append(lilDict)

    def getJsonifiedPassList(self):
        return json.dumps(self.passList)

if __name__ == '__main__':
    dpu = DataPrepUtil('./html', auto=1)
    print(dpu.fileList)
    print(dpu.getJsonifiedPassList())