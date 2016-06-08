import re
import time
from selenium import webdriver
class Baring(object):
    def __init__(self):
        self.url = 'http://www.baring.cn/quo/showmarket.html?m=us'
        self.driver = webdriver.Chrome('./chromedriver')
        self.driver.get(self.url)
        self.tableout = None
    def getCurrency(self, c):
        try:
            self.tableout = self.driver.find_element_by_id('quotation_grid')
        except BaseException:
            print 'Load one more time...'
            time.sleep(5)
            self.tableout = self.driver.find_element_by_id('quotation_grid')
        li = re.split('\n',self.tableout.text)
        for i in li:
            row = re.split(' ', i)
            if row[0] == c:
                return i
    def handleMessage(self, nex):
        print time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        print nex
    def doneInspect(self):
        print 'Done'
        self.driver.quit()
    def inspectCurrency(self, c):
        cur = ''
        heart_beat = 0
        while True:
            try:
                nex = self.getCurrency(c)
                rat = re.search('[0-9]*\.[0-9]*', nex).group()
                if cur != rat:
                    self.handleMessage(nex)
                    cur = rat
                    heart_beat = 0
                else:
                    heart_beat += 1
                if heart_beat > 100:
                    heart_beat = 0
                    self.driver.get(self.url)
                time.sleep(4)
            except KeyboardInterrupt:
                self.doneInspect()
                break
            except Exception:
                pass

c = 'USDCNY'
Baring().inspectCurrency(c)
