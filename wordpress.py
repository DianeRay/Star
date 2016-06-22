from selenium import webdriver
from selenium.webdriver.common.by import By
class Selenium(object):
    drivers = [None, './chromedriver', '../chromedriver', './chromedriver2.21']
    def init(self):
        for i in drivers:
            try:
                return webdriver.Chrome(i)
            except Exception:
                print 'Not found driver:'+i
    def getElementsByTagName(self, driver, tag):
        try:
            return driver.find_elements_by_tag_name(tag)
        except Exception:
            print 'No such a tag:'+tag
            return None
    def getElementsByClassName(self, driver, n):
        try:
            return driver.find_elements(By.CLASS_NAME, n)
        except Exception:
            print 'No such a CLASS_NAME!'+n
            return None
    def getElementById(self, driver, i):
        try:
            return driver.find_element_by_id(i)
        except Exception:
            print 'No such an ID'+i
            return None
    def getElementByCss(self, driver, css):
        try:
            return driver.find_element_by_css_selector(css)
        except Exception:
            print 'No such an ID'+css
            return None

class Wordpress(Selenium):
    def __init__(self, url):
        self.url = url
        self.driver = self.init()
        self.driver.get(self.url)
        
    def getArticles(self):
        return self.getElementsByTagName(self.driver, 'article')
    def getUrls(self, article_elements):
