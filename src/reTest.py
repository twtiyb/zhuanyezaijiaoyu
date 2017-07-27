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
    print(headers2)


# 要
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
        print(m.group())

# 取中间的值
def testRe2():
    testStr = 'var timingUrl = "http://hnwcf.59iedu.com/Home/Timing?usrId=cbbb39ba9a1541eba5828f540bb1641e&medId=hnzj201703160002&studyId=7e406fa82b584e7c9fe8c5af6200fff9"'
    m = re.search('"(\S*)"',testStr)[1]
    print(m)

# 取中间的值
def testRe3():
    testStr = '({"State":1,"Value":{"Process":40.0,"StudyTimeLength":1202,"OtherMediaName":"《打好河南的四张牌》02","OtherMedId":"hnzj201703160002","Type":1,"Message":null,"IsLoad":false},"Error":""})'
    # 正则
    m = re.search('\((\S*)\)',testStr)[1]
    print(m)
    testJson = json.loads(m)
    print(testJson)
    print(testJson['Value']['Process'])

# 取中间的值
def testRe4():
    courceContent = '({"State":1,"Value":{"Process":40.0,"StudyTimeLength":1202,"OtherMediaName":"《打好河南的四张牌》02","OtherMedId":"hnzj201703160002","Type":1,"Message":null,"IsLoad":false},"Error":""})'
    data = re.search('var mediaTime=.*', courceContent.text)[0]
    data = re.search('[0-9]*', data)[0]
    print(data);




# json操作
def testJson():
    jsonStr = u'{"State":1,"Value":{"Process":40.0,"StudyTimeLength":1202,"OtherMediaName":"ddd","OtherMedId":"hnzj201703160002","Type":1,"Message":null,"IsLoad":false},"Error":""}'
    print(jsonStr)

    testJson = json.loads(jsonStr)
    print(testJson)
    print(testJson['Value']['Process'])

    testJson = json.dumps(testJson)
    print(testJson)





if __name__ == '__main__':
    # testjs()
    # testRe()
    # testRe2()
    testRe3()
    # testJson()
# print execjs.eval("'red yellow blue'.split(' ')")


