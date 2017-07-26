import re
import json
import execjs


stra = 'function getStr(){var requestData = { CurrentTimespan: 0,  Id: "ea3faeed04ec4e749a244430bc4c445f",  SscId: "ed2181090bb6443e89bc565783974b96",SstId: "cd5eeb661b2c497ea629c43702f397dc",CourseSdlId: "40b64f1fccc2466fa30e7b2265a72527",TrainSdlId: "891b35fbe367417f8a4b0b3036ee96c0",Type: 1};return requestData;}'

# re.match("")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Referer': 'http://zjxy.hnhhlearning.com/Home',
    'Cookie': 'UM_distinctid=15d41670c242e8-018e214f8a9803-30667808-fa000-15d41670c25380; ASP.NET_SessionId=rqgvchrqa3x5flcmbl4fjtvt; hbjyUsersCookieszjxy.hnhhlearning.com=615|615|2f047a1d01464cb3ac2facd6eb01f3aa; IsLoginUsersCookies_zjxy.hnhhlearning.comzjxy.hnhhlearning.com=IsLogin; CNZZDATA1254133248=1011469955-1500039283-http%253A%252F%252Fzjpx.hnhhlearning.com%252F%7C1500899115Name'
}


def testjs():
    ctx = execjs.compile(stra)
    headers2 = ctx.call("getStr");
    print headers2


def testRe():
    pattern = re.compile('var requestData(.|\n)*?}')
    # match = pattern.match(str)
    # if match:
    #     print match.group()
    # m = re.match('var requestData(.|\n)*?}',stra)
    # if m:
    #     print m.group()

    m = re.search('var requestData(.|\n)*?}',stra)
    # m = re.match(pattern,stra)
    if m:
        print m.group()




if __name__ == '__main__':
    # testjs()
    testRe()
# print execjs.eval("'red yellow blue'.split(' ')")


