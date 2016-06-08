import re
import time
import md5
from selenium import webdriver
from selenium.webdriver.common.by import By
class Posts(object):
    def __init__(self):
        self.hash = {'title':0, 'author':1, 'comments':2, 'timestamp':3, 'hash_title_author':4, 'hash_author':5}
        self.data = [[],[],[],[],{},{}]
    def addPost(self, title, author, comments):
        hash_t_a = md5.new(title+author).digest()
        if hash_t_a in self.data[self.hash['hash_title_author']]:
            print 'Duplicated title & author found'
            title = title+'(dup)'
            hash_t_a = md5.new(title+author).digest()
        self.data[self.hash['title']].append(title)
        self.data[self.hash['author']].append(author)
        self.data[self.hash['comments']].append(re.search('[0-9]*',comments).group())
        self.data[self.hash['timestamp']].append(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
        self.data[self.hash['hash_title_author']][hash_t_a] = len(self.data[0])-1
        if author in self.data[self.hash['hash_author']]:
            self.data[self.hash['hash_author']][author].append(len(self.data[0])-1)
        else:
            self.data[self.hash['hash_author']][author] = [len(self.data[0])-1]
    def save(self):
        print self.data
        with open('log.txt', 'w') as f:
            records = len(self.data[0])
            f.write(str(records)+'\n')
            for j in xrange(len(self.data)):
                if type(self.data[j]) is list:
                    for i in xrange(records):
                        f.write(self.data[j][i]+'\n')
                elif type(self.data[j]) is dict:
                    for key, value in self.data[j].iteritems():
                        f.write(key+':'+str(value)+'\n')
    def load(self):
        with open('log.txt', 'r') as f:
            records = int(f.readline().strip('\n'))
            for j in xrange(len(self.data)):
                if type(self.data[j]) is list:
                    for i in xrange(records):
                        self.data[j].append(f.readline().strip('\n'))
                elif type(self.data[j]) is dict:
                    for i in xrange(records):
                        key, value = re.split(':', f.readline().strip('\n'))
                        self.data[j][key] = int(value)

class Reddit(object):
    def __init__(self):
        url = 'https://www.reddit.com/r/churning/'
        self.driver = webdriver.Chrome('../chromedriver2.21')
        self.driver.get(url)
        self.posts = Posts()
    def getElementByClassName(self, driver, n):
        try:
            return driver.find_elements(By.CLASS_NAME, n)
        except BaseException:
            print 'Load one more time...'+n
            time.sleep(5)
            return driver.find_elements(By.CLASS_NAME, n)
        except Exception:
            print 'No such a CLASS_NAME!'+n
            return None
    def getElementById(self, driver, id):
        try:
            return driver.find_element_by_id(id)
        except BaseException:
            print 'Load one more time...'+id
            time.sleep(5)
            return driver.find_element_by_id(id)
        except Exception:
            print 'No such an ID'+id
            return None
    def getTitles(self, sT):
        sitePosts = self.getElementByClassName(sT, 'title')
        titles = []
        for i in xrange(len(sitePosts)):
            cur = self.getElementByClassName(sitePosts[i], 'title')
            if cur:
                titles.append(cur[0].text)
        return titles
    def getAuthors(self, sT):
        tagLine = self.getElementByClassName(sT, 'tagline')
        authors = []
        for i in xrange(len(tagLine)):
            cur = self.getElementByClassName(tagLine[i], 'author')
            if cur:
                authors.append(cur[0].text)
        return authors
    def getComments(self, sT):
        flat_list = self.getElementByClassName(sT, 'flat-list')
        comments = []
        for i in xrange(len(flat_list)):
            cur = self.getElementByClassName(flat_list[i], 'comments')
            if cur:
                comments.append(cur[0].text)
        return comments
    def getList(self):
        siteTable = self.getElementById(self.driver, 'siteTable')
        titles = self.getTitles(siteTable)
        authors = self.getAuthors(siteTable)
        comments = self.getComments(siteTable)
        for i in xrange(len(titles)):
            self.posts.addPost(titles[i], authors[i], comments[i])
        self.posts.save()
        #self.posts.load()
    def done(self):
        print 'Done'
        self.driver.quit()

a = Reddit()
a.getList()
a.done()
