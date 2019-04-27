import bs4 as bs
import csv
import datetime
import os
import getpass
import json

class Extractor:

    def __init__(self, u, p, efficient=True):
        self.username = u
        self.password = p
        self.extractionError = False
        self.attendanceData = []
        self.marksData = []
        self.efficient = efficient

    def scrapeEverything(self):
        self.scrapeProfile()
        self.scrapeAcad()

    def scrapeProfile(self):
        try:
            print('[E] Scraping Profile...')
            with open('html/' + self.username + '/' + self.username + '_profile.html', 'r+') as f:
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
                with open('html/' + self.username + '/' + self.username + '_profile_data.csv', 'w+') as saveProf:
                    w = csv.DictWriter(saveProf, reqData.keys())
                    w.writeheader()
                    w.writerow(reqData)
        except:
            print('[E] [ERROR] Extraction Error in scrapeProfile()')
            self.extractionError = True

    def scrapeAcad(self):
        try:
            print('[E] Scraping Academics...')
            with open('html/' + self.username + '/' + self.username + '_academics.html', 'r+') as f:
                o = bs.BeautifulSoup(f.read(), features='html.parser')
                
                if self.efficient == False:
                    print('[E] \tFetching Enrollment Details...')
                    enrollmentDetailsData = {}
                    idFilter = len('ContentPlaceHolder1_lbl')
                    reqTags = o.find('div', attrs={'id':'1'}).find_all('span')
                    for i in reqTags:
                        newKey = i['id'][idFilter:]
                        newVal = i.text
                        enrollmentDetailsData[newKey] = newVal
                    with open('html/' + self.username + '/' + self.username + '_enrollment_data.csv', 'w+') as aed:
                        w = csv.DictWriter(aed, enrollmentDetailsData.keys())
                        w.writeheader()
                        w.writerow(enrollmentDetailsData)
                
                #Attendance
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
                self.attendanceData = attendanceData
                with open('html/' + self.username + '/' + self.username + '_attendance_data.csv', 'w+') as ad:
                    w = csv.DictWriter(ad, attendanceData[0].keys())
                    w.writeheader()
                    w.writerows(attendanceData)

                #Marks
                print('[E] \tFetching Marks Data...')
                table_div = o.find('div', id='accordion1').find_all('div', attrs={'class':'panel'})
                marklist = []
                for subject in table_div:
                    
                    sub_data = {} 
                    
                    # Subject Code
                    sub_code = subject.find('div', attrs={'class', 'panel-collapse'})['id']
                    sub_data['SubjectCode'] = sub_code

                    # Marks
                    sub_data['Marks'] = {}
                    table_marks = subject.find('div', attrs={'class', 'panel-collapse'}).find_all('table')
                    for table in table_marks:
                        
                        if table.find('th').text == 'Internal':
                            sub_data['Type'] = 'Theory'
                            sub_data['Marks']['Internals'] = []
                            #row
                            for tr in table.find_all('tr'):
                                test_marks = {}
                                #cell
                                for index, td in enumerate(tr.find_all('td')):
                                    scrap_material = td.string.replace("\n", "").strip(" ")
                                    if index == 0:
                                        if scrap_material == 'Total Marks':
                                            break
                                        test_marks['Test'] = scrap_material
                                    if index == 1:
                                        test_marks['MaxMarks'] = scrap_material
                                    if index == 2:
                                        test_marks['ObtainedMarks'] = scrap_material
                                if test_marks:
                                    sub_data['Marks']['Internals'].append(test_marks)
                            # print(sub_data['Internals'])
                                    
                        elif table.find('th').text == 'Assignment':
                            sub_data['Type'] = 'Theory'
                            sub_data['Marks']['Assignments'] = []
                            #row
                            for tr in table.find_all('tr'):
                                test_marks = {}
                                #cell
                                for index, td in enumerate(tr.find_all('td')):
                                    scrap_material = td.string.replace("\n", "").strip(" ")
                                    if index == 0:
                                        if scrap_material == 'Total Marks':
                                            break
                                        test_marks['Test'] = scrap_material
                                    if index == 1:
                                        test_marks['MaxMarks'] = scrap_material
                                    if index == 2:
                                        test_marks['ObtainedMarks'] = scrap_material
                                if test_marks:
                                    sub_data['Marks']['Assignments'].append(test_marks)

                        elif table.find('th').text == 'Lab':
                            sub_data['Type'] = 'Lab'
                            sub_data['Marks']['Lab'] = []
                            #row
                            for tr in table.find_all('tr'):
                                test_marks = {}
                                #cell
                                for index, td in enumerate(tr.find_all('td')):
                                    scrap_material = td.string.replace("\n", "").strip(" ")
                                    if index == 0:
                                        if scrap_material == 'Total Marks':
                                            break
                                        test_marks['Test'] = scrap_material
                                    if index == 1:
                                        test_marks['MaxMarks'] = scrap_material
                                    if index == 2:
                                        test_marks['ObtainedMarks'] = scrap_material
                                if test_marks:
                                    sub_data['Marks']['Lab'].append(test_marks)
                    
                    marklist.append(sub_data)
                self.marksData = marklist
                # print(json.dumps(marklist, indent=4, sort_keys=True))
                with open('html/' + self.username + '/' + self.username + '_marks_data.txt', 'w+') as md:
                    md.write(json.dumps(marklist, indent=4, sort_keys=True))

        except:
            print('[E] [ERROR] Extraction Error in scrapAcad()')
            self.extractionError = True


if __name__ == '__main__':
    un = input('UNAME ( NO ERROR )')
    myData = Extractor(un, '')
    myData.scrapeEverything()
