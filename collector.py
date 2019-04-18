import requests 
import os
import logging
import getpass
import extractor

#main vars
class Collector:
    targetUrl = 'https://slcm.manipal.edu/loginForm.aspx'
    username = ''
    password = ''
    loginPayload = {}
    htmlSavePath = 'html/'

    def __init__(self, u, p, efficient=True):
        self.setUserAndPass(u, p)
        self.setPayload()
        self.attendanceData = []
        self.errorDuringExtraction = False
        self.loginError = True
        self.collectionError = False
        self.efficient = efficient

    def setUserAndPass(self, u, p):
        self.username = u
        self.password = p

    def setPayload(self):
        self.loginPayload = {
            'txtUserid': self.username,
            'txtpassword': self.password,
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '/wEPDwULLTE4NTA1MzM2ODIPZBYCAgMPZBYCAgMPZBYCZg9kFgICAw8PFgIeB1Zpc2libGVoZGRkZQeElbA4UBZ/sIRqcKZDYpcgTP0=',
            '__VIEWSTATEGENERATOR': '6ED0046F',
            '__EVENTVALIDATION': '/wEdAAbdzkkY3m2QukSc6Qo1ZHjQdR78oILfrSzgm87C/a1IYZxpWckI3qdmfEJVCu2f5cEJlsYldsTO6iyyyy0NDvcAop4oRunf14dz2Zt2+QKDEIHFert2MhVDDgiZPfTqiMme8dYSy24aMNCGMYN2F8ckIbO3nw==',
            'btnLogin': 'Sign%20in'
    }

    def ensureHtmlDirExists(self):
        if os.path.isdir(self.htmlSavePath) == False:
            os.mkdir(self.htmlSavePath)

    def saveHtmlFile(self, code, appender):
        with open((self.htmlSavePath + self.username + os.sep + self.username + appender + '.html'), 'w+') as f:
            f.write(code.text)
            f.close()

    def gatherHtmlFiles(self, c):
        try:
            if self.efficient == False:
                feeDetailsCode = c.get('https://slcm.manipal.edu/FeeDetailsMIT.aspx')
                self.saveHtmlFile(feeDetailsCode, '_fees')
            studentProfileCode = c.get('https://slcm.manipal.edu/StudentProfile.aspx')
            academicsCode = c.get('https://slcm.manipal.edu/Academics.aspx')
            self.saveHtmlFile(studentProfileCode, '_profile')
            self.saveHtmlFile(academicsCode, '_academics')
        except:
            self.collectionError = True

    def makeReq(self):
        self.ensureHtmlDirExists()
        if os.path.isdir(self.htmlSavePath + self.username) == False:
            os.mkdir(self.htmlSavePath + self.username)

        with requests.Session() as c:
            try:
                res = c.post(self.targetUrl, data=self.loginPayload, headers={"Referer": "https://slcm.manipal.edu/loginForm.aspx"})
                if res.url.endswith('loginForm.aspx'): #login failure
                    self.loginError = True
                elif res.url.endswith('studenthomepage.aspx'): #login success
                    self.loginError = False
                    if self.efficient == False:
                        homePageCode = c.get('https://slcm.manipal.edu/studenthomepage.aspx')
                        self.saveHtmlFile(homePageCode, '_homepage')
                    self.gatherHtmlFiles(c)
                else:
                    self.loginError = True
            except:
                self.collectionError = True

            if self.loginError == False and self.collectionError == False:
                print('[C] Launching extractor...')
                newData = extractor.Extractor(self.username, self.password)
                newData.scrapeEverything()
                self.attendanceData = newData.attendanceData
                if newData.extractionError == True:
                    self.errorDuringExtraction = True
            else:
                if self.loginError:
                    print('[C] [ERROR] Login Error')
                if self.collectionError:
                    print('[C] [ERROR] Collection Error')
    
    def getErrorStatus(self):
        print("[C] [STATUS] LoginError: %s" % self.loginError)
        print("[C] [STATUS] CollectionError: %s" % self.collectionError)
        print("[C] [STATUS] ExtrationError: %s" % self.errorDuringExtraction)

if __name__ == '__main__':
    col = Collector('160905032', 'Eybitches')
    col.makeReq()
    col.getErrorStatus()