#urllib2在python3.x中被改为urllib.request
import urllib.request
import http.cookiejar
import urllib.parse

'''
urlopen(url, data, timeout),第一个参数url即为URL，第二个参数data是访问URL时要传送的数据，第三个timeout是设置超时时间。
'''
def openurl1():
    response = urllib.request.urlopen('http://www.baidu.com')
    return response


'''
或者:
urlopen参数可以传入一个request请求,它其实就是一个Request类的实例，构造时需要传入Url,Data等等的内容
'''
def openurl2():
    request = urllib.request.Request('http://www.baidu.com')
    try:
        response = urllib.request.urlopen(request)
    except urllib.request.HTTPError as e:
        print(e.reason)
    except urllib.request.URLError as e:
        print(e.reason)
    return response


'''
get和posts数据传送：针对动态网页，需要传递参数
get:直接以链接形式访问,链接中包含了所有的参数，当然如果包含了密码是一种不安全的选择
post:不会在网址上显示所有的参数，不过如果你想直接查看提交了什么就不太方便了
'''
#post
def openurl3():
    #设置文件头信息,Referer防盗链，服务器会识别headers中的referer是不是它自己
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'
    headers = { 'User-Agent' : user_agent,'Referer': 'http://www.csdn.net/'}

    values = {'username':'1142863292@qq.com', 'password':'6498liuqiao'}
    data = urllib.parse.urlencode(values)
    url = 'https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn'
    request = urllib.request.Request(url, data, timeout=10)
    response = urllib.request.urlopen(request)
    return response

#设置代理，网站可能会检测某一段时间某个IP 的访问次数，如果访问次数过多，它会禁止你的访问
def set_proxy():
    enable_proxy = True
    proxy_handler = urllib.request.ProxyHandler({"http" : 'http://some-proxy.com:8080'})
    null_proxy_handler = urllib.request.ProxyHandler({})
    if enable_proxy:
        opener = urllib.request.build_opener(proxy_handler)
    else:
        opener = urllib.request.build_opener(null_proxy_handler)
    urllib.request.install_opener(opener)


#get
def openurl4():
    values={}
    values['username'] = "1142863292@qq.com"
    values['password']="6498liuqiao"
    data = urllib.parse.urlencode(values)
    url = "http://passport.csdn.net/account/login"
    geturl = url + "?"+ data
    request = urllib.request.Request(geturl)
    response = urllib.request.urlopen(request, timeout=10)
    return response

'''
cookies的使用：cookielib(2),http.cookiejar(3)
cookie保存到变量中
'''
def get_cookie():
    #Cookiejar对象实例保存
    cookie = http.cookiejar.CookieJar()
    #创建cookie处理器
    handler = urllib.request.HTTPCookieProcessor(cookie)
    #通过handler构建opener
    opener = urllib.request.build_opener(handler)

    request = urllib.request.Request("http://www.baidu.com")
    response = opener.open(request,timeout=10)

    for item in cookie:
        print(item.name + ' : ' + item.value)

'''
保存cookie到文件中
'''
def get_cookie_to_file():
    filename = 'cookie.txt'
    #MozillaCookieJar对象保存cookie，之后写入文件
    cookie = http.cookiejar.MozillaCookieJar(filename)
    #生成cookie处理器
    handler = urllib.request.HTTPCookieProcessor(cookie)
    #创建opener
    opener = urllib.request.build_opener(handler)
    response = opener.open("http://www.baidu.com")
    # ignore_discard的意思是即使cookies将被丢弃也将它保存下来，ignore_expires的意思是如果在该文件中cookies已经存在，则覆盖原文件写入
    cookie.save(ignore_discard = True, ignore_expires = True)

'''
从文件中获取cookie并使用
'''
def get_cookie_from_file():
    #创建cookie变量并从文件中读取cookie内容到变量
    cookie = http.cookiejar.MozillaCookieJar()
    cookie.load('cookie.txt', ignore_expires = True, ignore_discard = 'True')
    #创建request
    request = urllib.request.Request('http://www.baidu.com')
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
    response = opener.open(request)
    print(response.read())

'''
使用cookie模拟登录网站
'''
def login_using_cookie():
    filename = 'cookie.txt'
    cookie = http.cookiejar.MozillaCookieJar(filename)
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
    postdata = urllib.parse.urlencode({'username':'liu462016300', 'password':'6498liuqiao', 'rememberMe':'true'}).encode(encoding='utf8')
    loginurl = 'https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn'

    try:
        result = opener.open(loginurl, postdata,timeout=10)
        cookie.save(ignore_expires=True, ignore_discard=True)
        print(result.read().decode('utf-8'))
    except urllib.request.HTTPError as e:
        print(e.reason)
        print(e.code)
    except urllib.request.URLError as e:
        print(e.reason)
    except Exception as e:
        print(e)


    print('--------------------------------------------')
    otherurl = 'http://write.blog.csdn.net/postlist'

    try:
         result = opener.open(otherurl)
         print(result.read().decode('utf-8'))
    except urllib.request.HTTPError as e:
        print(e.reason)
        print(e.code)
    except urllib.request.URLError as e:
        print(e.reason)
    except Exception as e:
        print(e)



if __name__ == '__main__':
    #response = openurl2()
    #response = openurl3()
    #response = openurl4()
    #print(response.read())
    #get_cookie_to_file()
    #get_cookie_from_file()
    login_using_cookie()






















