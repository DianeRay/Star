import time
import os
author = ' Ray:'
with open('README.txt','a+w') as f:
	f.write('\n'+time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())+author+'\n')
os.system('vi README.txt')
