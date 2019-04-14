import requests 
import os
import logging
import getpass
import extractor

#main vars
class Collector:
    initUrl = 'https://slcm.manipal.edu/loginForm.aspx'
    username = '160905032'
    password = 'Eybitches'
    loginPayload = {}
    htmlSavePath = 'html/'

    def __init__(self, u, p):
        self.setUserAndPass(u, p)
        self.setPayload()
        self.errorDuringExtraction = False

    def setUserAndPass(self, u, p):
        if u != '':
            self.username = u
        if p != '':
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

    def saveHtmlFile(self, code, appender):
        saveHtml = open((self.username + appender + '.html'), 'w+')
        saveHtml.write(code.text)
        saveHtml.close()

    def gatherHtmlFiles(self, c):
        studentProfileCode = c.get('https://slcm.manipal.edu/StudentProfile.aspx')
        academicsCode = c.get('https://slcm.manipal.edu/Academics.aspx')
        feeDetailsCode = c.get('https://slcm.manipal.edu/FeeDetailsMIT.aspx')
        self.saveHtmlFile(studentProfileCode, 'profile')
        self.saveHtmlFile(academicsCode, 'academics')
        self.saveHtmlFile(feeDetailsCode, 'fees')

    def makeReq(self):
        if os.path.isdir(self.htmlSavePath + self.username) == False:
            os.mkdir(self.htmlSavePath + self.username)
        os.chdir(self.htmlSavePath + self.username)

        with requests.Session() as c:
            logging.debug('LOGGING IN')
            c.post(self.initUrl, data=self.loginPayload, headers={"Referer": "https://slcm.manipal.edu/loginForm.aspx"})
            logging.debug('WE ARE IN')
            homePageCode = c.get('https://slcm.manipal.edu/studenthomepage.aspx')
            self.saveHtmlFile(homePageCode, '')
            logging.debug('START MAKING HTML FILES')
            self.gatherHtmlFiles(c)
            logging.debug('COMPLETE')
            print('Logging out...')
            c.get('https://slcm.manipal.edu/loginForm.aspx')
        
        print('Starting extractor...')
        print('Going to root directory from current directory ' + os.getcwd())
        os.chdir('../..')
        print('cwd: ' + os.getcwd())
        newData = extractor.ExtractInstance(self.username, self.password)
        newData.scrapeEverything()
        if newData.extractionError == True:
            self.errorDuringExtraction = True

if __name__ == '__main__':
    col = Collector('160905032', 'Eybitches')
    col.makeReq()
