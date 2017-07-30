import requests
import execjs
import re
import json
import sqlite3


from bs4 import BeautifulSoup as bs

domin = 'http://zjxy.hnhhlearning.com'
homeUrl = 'http://zjxy.hnhhlearning.com/Home'
learningUrl = 'http://zjxy.hnhhlearning.com/Study/Learning?'
learningMediaLiUrl = 'http://zjxy.hnhhlearning.com/Study/Learning/MediaLi?'
answers = 'http://zjxy.hnhhlearning.com/Study/ExamList/TestHistory'

s = requests.Session()

# 构造header头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Referer': 'http://zjxy.hnhhlearning.com/Home',
    'Cookie': 'UM_distinctid=15d41670c242e8-018e214f8a9803-30667808-fa000-15d41670c25380; CNZZDATA1254133248=1011469955-1500039283-http%253A%252F%252Fzjpx.hnhhlearning.com%252F%7C1501175262; ASP.NET_SessionId=zlx3fyl1gtkxrjmjpqgzb5uv; hbjyUsersCookieszjxy.hnhhlearning.com=615|615|2f047a1d01464cb3ac2facd6eb01f3aa; IsLoginUsersCookies_zjxy.hnhhlearning.comzjxy.hnhhlearning.com=IsLogin'
}

# 登陆到home
homeData = s.get(homeUrl, headers=headers)
homeContent = bs(homeData.content, 'lxml')


# 获取子课程
def getChildCources(sscId):
    courceData = s.get(learningUrl + 'sscId=' + sscId, headers=headers)
    courceContent = bs(courceData.content, 'lxml')

    child_cources_list = []
    for idx, tr in enumerate(courceContent.select(".xktable tbody tr")):
        tds = tr.select('td')
        percent = tds[2].contents[1]['src']
        percent = percent[percent.find('id=') + 3:]
        url = tds[3].contents[1]['href']
        medId = url[url.find('medId=') + 6:]

        child_cources_list.append({
            '子课程名称': tds[0].contents[0],
            '学习进度': percent,
            'url': url,
            'medId': medId
        })
    return child_cources_list


# 获取主课程
def getMainCources(homeContent):
    cources_list = []
    for idx, tr in enumerate(homeContent.select(".homelinetable-dashed-bom tr")):
        if idx != 0:
            tds = tr.select('td')
            percent = tds[2].contents[1]['src']
            percent = percent[percent.find('id=') + 3:]
            url = tds[3].contents[1]['href']
            sscId = url[url.find('sscId=') + 6:]

            cources_list.append({
                '课程名称': tds[0].contents[0],
                '学时': tds[1].contents[0],
                '学习进度': percent,
                'url': url,
                'sscId': sscId,
                '全部课程': getChildCources(sscId)
            })
    return cources_list


# 提交进度
def pushPercent(sscId, medId):
    courceData = s.get(learningMediaLiUrl + 'sscId=' + sscId + '&medId=' + medId, headers=headers)
    courceContent = bs(courceData.content, 'lxml')

    # 获取pushPercent参数
    m = re.search('var requestData =(.|\n)*?}', courceContent.text)
    data = m.group()
    data = data.replace("RequestType.Offen", "1")
    jsStr = 'function getObj(){' + data + ';return requestData;}'
    ctx = execjs.compile(jsStr)
    pushParams = ctx.call("getObj")
    pushParams['CurrentLength'] = 30

    data = re.search('var mediaTime=.*', courceContent.text)[0]
    data = re.search('[0-9]*', data)[0]
    pushParams['CurrentTimespan'] = 3000


    # 获取pushPercent url
    m = re.search('var timingUrl = ".*?"', courceContent.text)
    data = m.group()
    pushUrl = re.search('"(\S*)"', data)[1]

    # 拼接参数
    # type == 2 代表开始
    pushParams['Type'] = 2
    courceData = s.get(pushUrl + 'sscId=' + sscId + '&medId=' + medId, params=pushParams, headers=headers)
    testStr = courceData.text
    result = json.loads(re.search('\((\S*)\)', testStr)[1]);

    print('完成' + str(result['Value']['Process']))

    # type == 1 代表持续,类似于心跳...网站这里必须是先开始,然后再发心跳,才能增加进度.所以先要设置成2请求一次,再设置成1持续请求
    pushParams['Type'] = 1
    while(result['Value']['Process'] < 100):
        courceData = s.get(pushUrl + 'sscId=' + sscId + '&medId=' + medId, params=pushParams, headers=headers)
        testStr = courceData.text
        result = json.loads(re.search('\((\S*)\)', testStr)[1]);
        print('完成' + str(result['Value']['Process']))
        # requestData =

# 提交学习进度
def learn():
    cources_list = getMainCources(homeContent)
    for cource in cources_list:
        for childCource in cource['全部课程']:
            if int(childCource['学习进度']) == 100:
                print(childCource['子课程名称'] + ':已经学习过,不需要学习')
                continue
            print(childCource['子课程名称'] + ':开始学习')
            pushPercent(cource['sscId'], childCource['medId'])



# 从练习记录中获取考试答案,保存到数据库中
def getsAnswers():
    answersHomeData = s.get(homeUrl, headers=headers)
    answersHomeContent = bs(answersHomeData.content, 'lxml')
    for idx, tr in enumerate(answersHomeContent.select(".listtable tbody tr")):


        sqlStr = '''INSERT INTO Exam (exam_id, name) VALUES ('{0}','{1}')'''.format(str(tr.contents[1]['value']),str(tr.contents[1].text))
        execSql(sqlStr)
    print('ss')



# todo 直接读取目录下的数据库脚本来创建数据库,目前直接用其他方式创建数据库
def createSqliteDb():
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE category
          (id int primary key, sort int, name text)''')
    c.execute('''CREATE TABLE book
          (id int primary key,
           sort int,
           name text,
           price real,
           category int,
           FOREIGN KEY (category) REFERENCES category(id))''')
    conn.commit()
    conn.close()

# todo 真是浪费,后边使用orm框架来操作数据库
def execSql(sqlStr):
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    c.execute(sqlStr)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    getsAnswers()
    # createSqliteDb();
    print()
