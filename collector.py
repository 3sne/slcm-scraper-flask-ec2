import requests 
import os
import logging
import getpass
import extractor
import bs4 as bs

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
        try:
            res = requests.get(self.targetUrl)
            print("SUCCC" , res.url)
            soup = bs.BeautifulSoup(res.text, features='html.parser')
            ext_vs = soup.select_one('#__VIEWSTATE')['value']
            ext_vsg = soup.select_one('#__VIEWSTATEGENERATOR')['value']
            ext_ev = soup.select_one('#__EVENTVALIDATION')['value']
            self.loginPayload = {
                'txtUserid': self.username,
                'txtpassword': self.password,
                '__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                '__VIEWSTATE': ext_vs,
                '__VIEWSTATEGENERATOR': ext_vsg,
                '__EVENTVALIDATION': ext_ev,
                'btnLogin': 'Sign%20in'
        }
        except:
            print('[C] Payload setting failed')
            self.loginError = True


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
        with requests.Session() as c:
            try:
                res = c.post(self.targetUrl, data=self.loginPayload, headers={"Referer": "https://slcm.manipal.edu/loginForm.aspx"})
                if res.url.endswith('loginForm.aspx'): #login failure
                    self.loginError = True
                elif res.url.endswith('studenthomepage.aspx'): #login success
                    self.loginError = False
                    if os.path.isdir(self.htmlSavePath + self.username) == False:
                        os.mkdir(self.htmlSavePath + self.username)
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
                self.marksData = newData.marksData
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