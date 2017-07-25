import requests
import execjs
import re


from bs4 import BeautifulSoup as bs

domin = 'http://zjxy.hnhhlearning.com'
homeUrl = 'http://zjxy.hnhhlearning.com/Home'
s = requests.Session()

# 构造header头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Referer': 'http://zjxy.hnhhlearning.com/Home',
    'Cookie': 'UM_distinctid=15d41670c242e8-018e214f8a9803-30667808-fa000-15d41670c25380; ASP.NET_SessionId=rqgvchrqa3x5flcmbl4fjtvt; hbjyUsersCookieszjxy.hnhhlearning.com=615|615|2f047a1d01464cb3ac2facd6eb01f3aa; IsLoginUsersCookies_zjxy.hnhhlearning.comzjxy.hnhhlearning.com=IsLogin; CNZZDATA1254133248=1011469955-1500039283-http%253A%252F%252Fzjpx.hnhhlearning.com%252F%7C1500899115Name'
}

# 登陆到home
homeData = s.get(homeUrl, headers=headers)
homeContent = bs(homeData.content, 'lxml')


# 获取子课程
def getChildCources(url):
    courceData = s.get(domin + url, headers=headers)
    courceContent = bs(courceData.content, 'lxml')

    child_cources_list = []
    for idx, tr in enumerate(courceContent.select(".xktable tbody th")):
        tds = tr.select('td')
        percent = tds[2].contents[1]['src']
        percent = percent[percent.find('id=') + 3:]
        url = tds[3].contents[1]['href']
        medId = url[url.find('medId=') + 6:]

        child_cources_list.append({
            '课程名称': tds[0].contents[0],
            '学习进度': percent,
            'url': url,
            'medId': medId
        })
    return  child_cources_list



#获取主课程
def getMainCources(homeContent):
    cources_list = []
    for idx, tr in enumerate(homeContent.select(".homelinetable-dashed-bom tr")):
        if idx != 0:
            tds = tr.select('td')
            percent = tds[2].contents[1]['src']
            percent = percent[percent.find('id=')+3:]
            url = tds[3].contents[1]['href']
            sscId = url[url.find('sscId=')+6:]

            cources_list.append({
                '课程名称': tds[0].contents[0],
                '学时': tds[1].contents[0],
                '学习进度': percent,
                'url': url,
                'sscId':sscId,
                '全部课程': getChildCources(url)
            })
    return cources_list




#提交进度
def pushPercent(url):
    courceData = s.get(domin+url, headers=headers)
    courceContent = bs(courceData.content,'lxml')
    re.match('{(. |\n) *}',courceContent.text)

    jsStr = ""

    requestData = ;




if __name__ == '__main__':
    cources_list = getMainCources(homeContent)
    for cource in cources_list:
        for childCource in cource:
            if cource['学习进度'] < 100:
                print(childCource['课程名称:'] + '已经学习过,不需要学习')
            print(childCource['课程名称:'] + '开始学习')
            pushPercent(childCource['url'])










