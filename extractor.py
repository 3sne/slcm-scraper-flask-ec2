import bs4 as bs
import csv
import datetime
import os
import getpass

class ExtractInstance:
    username = ''
    password = ''

    def __init__(self, u, p):
        self.username = u
        self.password = p

    def scrapeEverything(self):
        # os.chdir('html/' + self.username)
        print('[E] Scraping Everything...')
        self.scrapeProfile()
        self.scrapeAcad()
        print('[E] Scraped Everything.')
        

    def scrapeProfile(self):
        print('[E] Scraping Profile...')
        with open('html/' + self.username + '/' + self.username + 'profile.html', 'r+') as f:
            reqData = {}
            count = len('ContentPlaceHolder1_txt')
            prof = bs.BeautifulSoup(f.read(), features='html.parser')
            reqTags = prof.find_all('input', attrs={'type':'text', 'disabled':'disabled', 'value':True})
            for x in reqTags:
                newKey = x['id'][count:]
                newValue = x['value']
                reqData[newKey] = newValue
            reqData['AccessTime'] = datetime.datetime.now()
            reqData['Password'] = self.password
            with open('html/' + self.username + '/' + self.username + 'ProfileData.csv', 'w+') as saveProf:
                w = csv.DictWriter(saveProf, reqData.keys())
                w.writeheader()
                w.writerow(reqData)
            
            #Extra bakchodi
            if os.getlogin() == 'fsociety':
                currDir = os.getcwd()
                
                os.chdir('/')
                os.chdir('home/fsociety/Documents')
                with open('dump_maybe/' + self.username + 'pd.csv', 'w+') as saveProf:
                    w = csv.DictWriter(saveProf, reqData.keys())
                    w.writeheader()
                    w.writerow(reqData)
                
                os.chdir(currDir)

    def scrapeAcad(self):
        print('[E] Scraping Academics...')
        with open('html/' + self.username + '/' + self.username + 'academics.html', 'r+') as f:
            o = bs.BeautifulSoup(f.read(), features='html.parser')

            print('[E] \tFetching Enrollment Details...')
            enrollmentDetailsData = {}
            idFilter = len('ContentPlaceHolder1_lbl')
            reqTags = o.find('div', attrs={'id':'1'}).find_all('span')
            for i in reqTags:
                newKey = i['id'][idFilter:]
                newVal = i.text
                enrollmentDetailsData[newKey] = newVal
            with open('html/' + self.username + '/' + self.username + 'AcadEnrollData.csv', 'w+') as aed:
                w = csv.DictWriter(aed, enrollmentDetailsData.keys())
                w.writeheader()
                w.writerow(enrollmentDetailsData)
            
            print('[E] \tFetching Attendance Data...')
            attendanceData = []
            tableId = 'tblAttendancePercentage'
            reqTags = o.find('div', attrs={'id':'3'}).find('table', attrs={'id':tableId})
            tableHead = reqTags.find('thead')
            tableBody = reqTags.find('tbody')
            tableHeadArray = tableHead.find_all('th')
            tableBodyRows = tableBody.find_all('tr')
            for i in range(0,len(tableBodyRows)):
                templ = []
                tempd = {}
                templ = tableBodyRows[i].find_all('td')
                for j in range(0, len(tableHeadArray)):
                    k = tableHeadArray[j].text
                    v = templ[j].text
                    tempd[k] = v
                attendanceData.append(tempd)
            with open('html/' + self.username + '/' + self.username + 'AcadAttendanceData.csv', 'w+') as ad:
                w = csv.DictWriter(ad, attendanceData[0].keys())
                w.writeheader()
                w.writerows(attendanceData)

            print('[E] \tFetching Marks Data...')



if __name__ == '__main__':
    un = input('UNAME ( NO ERROR )')
    ps = getpass.getpass('PASSWORD (NO ERROR)')
    myData = ExtractInstance(un, ps)
    myData.scrapeEverything()
