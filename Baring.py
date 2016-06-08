#This script only extracts one record from the Baring.cn
import time
import re
from selenium import webdriver

driver = webdriver.Chrome('../chromedriver2.21')  # Optional argument, if not specified will search path.
driver.get('http://www.baring.cn/quo/showmarket.html?m=us');
try:
    tableout = driver.find_element_by_id('quotation_grid')
except BaseException:
    time.sleep(5)
    print 'Loading...'
    tableout = driver.find_element_by_id('quotation_grid')
curr = 0
while True:
    time.sleep(4)
    li = re.split('\n',tableout.text)
    for i in li:
        row = re.split(' ', i)
        if row[0] == 'USDCAD' and curr != row[2]:
            print time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            print i
            curr = row[2]
