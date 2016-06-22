import re
import time
import md5
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
class Selenium(object):
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

class Posts(object):
    def __init__(self):
        self.hash = {'title':0, 'author':1, 'comments':2, 'timestamp':3, 'hash_title_author':4, 'hash_author':5, 'url':6}
        self.data = [[],[],[],[],{},{},[]]
        self.post_threads = []
    def my_random_string(self, string_length=10):
        """Returns a random string of length string_length."""
        rand = str(uuid.uuid4()) # Convert UUID format to a Python string.
        rand = rand.replace("-","") # Remove the UUID '-'.
        return rand[0:string_length] # Return the random string.
    def addPost(self, title, author, comments, url, driver, details):
        hash_t_a = md5.new(title+author).digest()
        if hash_t_a in self.data[self.hash['hash_title_author']]:
            print 'Duplicated title & author found'
            title = title+'(dup)'+self.my_random_string()
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
        self.data[self.hash['url']].append(url)
        if details:
            self.post_threads.append(Post_threads(url, driver))
    def save(self):
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

class Post_comment(object):
    def __init__(self):
        self.author = ''#self.getAuthor(self.getElementByCss(driver, 'div.entry'))
        self.text = ''#self.getText(self.getElementByCss(driver, 'div.entry'))
        self.next = []#self.getChildren(self.getElementByCss(driver, 'div.child'))

class Post_threads(Selenium):
    def __init__(self, url, driver):
        self.url = url
        driver.get(self.url)
        self.driver = driver
        self.content = self.getElementByCss(self.driver, 'div.content')
        self.comments = Post_comment()
        self.getComments()
    def getAuthor(self, driver):
        try :
            author = self.getElementByCss(driver, 'a.author')
            return author.text.encode('utf8')
        except Exception:
            return None
    def getText(self, driver):
        try:
            user_text = self.getElementByCss(driver, 'div.usertext-body.md-container')
            return user_text.text.encode('utf8')
        except Exception:
            return None
    def getNodesDFS(self, siteTable):
        if siteTable == None:
            return None
        siteTable_name = siteTable.get_attribute('id')
        de = []
        #print self.getElementByCss(self.getElementById(siteTable,siteTable_name), ':first-child')
        while self.getElementByCss(self.getElementById(siteTable,siteTable_name), ':first-child') != None:
            parent_driver = self.getElementByCss(siteTable,'div.thing')
            cur = Post_comment()
            if parent_driver:
                cur.author = self.getAuthor(parent_driver)
                cur.text = self.getText(parent_driver)
                child = self.getElementByCss(parent_driver, 'div.child')
                siteTable_next = self.getElementByCss(child, 'div[id^="siteTable"]')
                cur.next = self.getNodesDFS(siteTable_next)
                if cur.author is not None:
                    de.append(cur)
            try:
                self.driver.execute_script('document.getElementById("'+siteTable_name+'").removeChild(document.getElementById("'+siteTable_name+'").firstChild)')
            except Exception:
                pass
        return de
    def getComments(self):
        domains = re.split('/',self.url)
        if 'www.reddit.com' in domains:
            siteTable = self.getElementById(self.content, 'siteTable')
            self.comments.text = self.getElementByCss(siteTable, 'div.usertext-body').text
            self.comments.next = self.getNodesDFS(self.getElementByCss(self.getElementByCss(self.content, 'div.commentarea'), 'div[id^="siteTable_t3"]'))
            self.save()
    def save(self):
        appendix = re.split('/',self.url)
        with open(appendix[-3]+'-'+appendix[-2]+'-log-comments.txt', 'w+') as f:
            def saveDFS(node, level):
                if node.next == None:
                    return
                for i in node.next:
                    try:
                        f.write(str(level).encode('utf8')+'-'+i.author.encode('utf8')+'\n'+i.text.encode('utf8')+'\n')
                    except Exception:
                        f.write(str(level).encode('utf8')+'-error\nerror\n')
                    saveDFS(i, level+1)
            f.write('-1-'+self.comments.author.encode('utf8')+'\n'+self.comments.text.encode('utf8'))
            saveDFS(self.comments, 0)
    def load(self):
        pass

class Reddit(Selenium):
    def __init__(self, url):
        self.url = url
        try:
            self.driver = webdriver.Chrome()
        except Exception:
            print 'Not found Chrome driver'
            self.driver = webdriver.Chrome('./chromedriver')
        self.posts = Posts()
    def getTitles(self, sT):
        sitePosts = self.getElementsByClassName(sT, 'title')
        titles = []
        for i in xrange(len(sitePosts)):
            cur = self.getElementsByClassName(sitePosts[i], 'title')
            if cur:
                titles.append(cur[0].text.encode('utf8'))
        return titles
    def getAuthors(self, sT):
        tagLine = self.getElementsByClassName(sT, 'tagline')
        authors = []
        for i in xrange(len(tagLine)):
            cur = self.getElementsByClassName(tagLine[i], 'author')
            if cur:
                authors.append(cur[0].text.encode('utf8'))
        return authors
    def getComments(self, sT):
        flat_list = self.getElementsByClassName(sT, 'flat-list')
        comments = []
        for i in xrange(len(flat_list)):
            cur = self.getElementsByClassName(flat_list[i], 'comments')
            if cur:
                comments.append(cur[0].text)
        return comments
    def getUrls(self, sT):
        sitePosts = self.getElementsByClassName(sT, 'title')
        urls = []
        for i in xrange(len(sitePosts)):
            cur = self.getElementsByClassName(sitePosts[i], 'title')
            if cur:
                urls.append(cur[0].get_attribute('href'))
        return urls
    def getNextPage(self, url):
        try:
            self.driver.get(url)
            next_button = self.getElementByCss(self.getElementByCss(self.driver, 'div.nav-buttons'), 'a[rel~="next"]')
            return next_button.get_attribute('href')
        except Exception:
            print 'Next page not found'
            return None
    def updateCatagory(self, details):
        cur = self.url
        while cur:
            try:
                self.getList(cur, details)
                cur = self.getNextPage(cur)
            except Exception:
                time.sleep(5)
    def getList(self, url, details):
        self.driver.get(url)
        siteTable = self.getElementById(self.driver, 'siteTable')
        titles = self.getTitles(siteTable)
        authors = self.getAuthors(siteTable)
        comments = self.getComments(siteTable)
        urls = self.getUrls(siteTable)
        for i in xrange(len(titles)):
            self.posts.addPost(titles[i], authors[i], comments[i], urls[i], self.driver, details)
    def done(self):
        print 'Done'
        self.posts.save()
        self.driver.quit()

details = False
a = Reddit('https://www.reddit.com/r/churning/')
a.updateCatagory(details)
a.done()
