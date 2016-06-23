import re
from db import db
from selenium import webdriver
from selenium.webdriver.common.by import By
class Selenium(object):
    def init(self):
        drivers = ['./chromedriver', '../chromedriver', './chromedriver2.21']
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
            return []
    def getElementByTagName(self, driver, tag):
        try:
            return driver.find_element_by_tag_name(tag)
        except Exception:
            print 'No such a tag:'+tag
            return None
    def getElementsByClassName(self, driver, n):
        try:
            return driver.find_elements(By.CLASS_NAME, n)
        except Exception:
            print 'No such a CLASS_NAME!'+n
            return []
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
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()
    def loadUrl(self, driver, url):
        try:
            driver.get(url)
            return True
        except Exception:
            print 'unable to get page:'+url
            return False
    def getArticles(self, element):
        return self.getElementsByTagName(element, 'article')
    def getMain(self, element):
        return self.getElementById(element, 'main')
    def getUrl(self, element):
        return self.getElementByTagName(element, 'a').get_attribute('href').encode('utf8')
    def getText(self, element):
        return element.text.encode('utf8')
    def getComment(self, aside):
        return re.search('\([0-9]*\)', aside).group().lstrip('(').rstrip(')').encode('utf8')
    def getPostTime(self, aside):
        return re.search('[0-9]* [a-zA-Z]* [0-9]*', aside).group().encode('utf8')
    def getTitle(self, element):
        return self.getText(self.getElementByTagName(element, 'a'))
    def getImgUrl(self, element):
        return self.getElementByTagName(element, 'img').get_attribute('src')
    def getPostThumb(self, element):
        return self.getElementByCss(element, 'div.post-thumb')
    def getPostAside(self, element):
        return self.getElementByCss(element, 'aside.post-aside')
    def getNextPageUrl(self, element):
        nav = self.getElementByCss(self.driver, 'div.col-md-12')
        return self.getElementByCss(nav, 'a.next').get_attribute('href').encode('utf8')
    def parse(self, max_pages):
        url = self.url
        for _ in xrange(max_pages):
            data = []
            if self.loadUrl(self.driver, url) is False:
                break
            articles = self.getArticles(self.getMain(self.driver))
            for i in articles:
                aside = self.getText(self.getPostAside(i))
                print aside
                data.append([('title', self.getTitle(i), 'varchar'), \
                             ('url', self.getUrl(i), 'varchar'), \
                             ('post_type', 'Video', 'varcahr'), \
                             ('img_url', self.getImgUrl(self.getPostThumb(i)), 'varchar'), \
                             ('comment', self.getComment(aside), 'bigint'), \
                             ('post_time', self.getPostTime(aside), 'varchar')])
            with db('test_wordpress', '192.168.1.191', 'ray1', 'abc19910601') as mysql_db:
                for i in data:
                    mysql_db.insert_db('pages', i)

if __name__ == '__main__':
    with Wordpress('') as a:
        a.parse(1)
