#coding:utf-8
import urllib.request
import urllib.parse
import re
import subprocess

class QSBK:
    def __init__(self):
        self.__pageIndex = 1
        self.__user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'
        self.__header = {'User-Agent' : self.__user_agent}
        self.__enable = True
        self.__stories = []

    @property
    def pageIndex(self):
        return self.__pageIndex

    @pageIndex.setter
    def pageIndex(self, value):
        self.__pageIndex = value
        
    @property
    def stories(self):
        return self.__stories
    
    @stories.setter
    def stories(self, value):
        self.__stories = value

    @property
    def enable(self):
        return self.__enable

    @enable.setter
    def enable(self, value):
        self.__enable = value;

    def get_page(self):
        url = 'http://www.qiushibaike.com/textnew/page/' + str(self.__pageIndex)
        try:
            request = urllib.request.Request(url, headers = self.__header)
            response = urllib.request.urlopen(request)
            context = response.read().decode('utf-8')
            pattern = re.compile(r'<div class="author clearfix">.*?<h2>(.*?)</h2>.*?<div class="content">(.*?)</div>.*?<i class="number">(.*?)</i>.*?<i class="number">(.*?)</i>', re.S)
            self.__stories = re.findall(pattern, context)
        except urllib.request.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)

    def is_continue(self,result):
        if result == 'n' or result == 'N':
            self.__enable = False
            exit(0)
        else:
            return True

    def list_in_current_page(self):
        index = 0
        for item in self.__stories:
            if index % 4 == 0:
                subprocess.call('cls', shell=True)
            print('----------------------------------------------------------')
            print("发帖人：" + item[0] + "  好笑：" + item[2] + "  评论：" + item[3])
            print(item[1].replace('<br/>', '\n'))
            print('--------------------当前第%d页---%d/%d----------------------' % (self.__pageIndex, index+1, len(self.__stories)))
            result = input("查看下一个(enter/n)")
            while not self.is_continue(result):
                result = input('输入错误，请重新输入(enter/n):')
            index += 1

    def start(self):
        while(self.__enable):
            self.get_page()
            self.list_in_current_page()
            result = input('当前页的段子已看完，是否继续(enter/n):')
            while not self.is_continue(result):
                result = input('输入错误，请重新输入(enter/n):')
            self.__stories = []
            self.__pageIndex += 1

if __name__ == '__main__':
    spider =  QSBK()
    spider.start()