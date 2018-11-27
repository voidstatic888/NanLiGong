
# coding: utf-8

# In[84]:


from PIL import Image
import pytesseract
import sys
import os
import heapq
import random
import re
import requests
import json
import time
import concurrent.futures


# In[129]:


headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Host' : 'dxyq.njust.edu.cn',
    'Proxy-Connection' : 'keep-alive',
    'Referer' : 'http://dxyq.njust.edu.cn/norderday.jsp?equipId=4af7d10b44723d690144726efb330007&time=1543507200000&ro=false',
    'Origin' : 'http://dxyq.njust.edu.cn',
    'Accept' : 'application/json, text/javascript, */*',
    'Accept-Language' : 'zh-CN,zh;q=0.9',
    'Accept-Encoding' : 'gzip, deflate'
}

proxies = {
    'http': 'http://xzproxy.cnsuning.com:8080',
    'https': 'https://xzproxy.cnsuning.com:8080'
}

getImageHeaders = {
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Upgrade-Insecure-Requests' : '1',
    'Proxy-Connection' : 'keep-alive',
    'Pragma' : 'no-cache',
    'Accept-Language' : 'zh-CN,zh;q=0.9',
    'Accept-Encoding' : 'gzip, deflate',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Host' : 'dxyq.njust.edu.cn'
}

cookies = {
    'JSESSIONID' : 'C443724173F1ED93C976D7C8A314A722',
    'iPlanetDirectoryPro' : 'dk3Jfhy2rQCSKbDuqbg6bt',
    'MOD_AUTH_CAS' : 'MOD_AUTH_ST-229670-BKcMOTddIlqhgtdT9WPB1543304275052-bhIs-cas',
}

params = {
    'equipId' : '4af7d10b44723d690144726efb330007',
    'startDate' : '2018-12-4 19:00',
    'endDate' : '2018-12-4 20:00',
    'content' : 'testtesttesttesttest',
    'noMerge' : 'false',
    'operatorType' : '1',
    'userno' : '',
    'validate' : ''
}

errorMap = {
    '82 79' : '8279',
    '444a' : '4448',
    '43 72' : '4372',
    '93 76' : '9376'
}
 
#二值化,输入阈值和文件地址
def binaryzation(threshold,image_address):
    image=Image.open(image_address)#打开图片
    image=image.convert('L')#灰度化
    table=[]
    for x in range(256):#二值化
        if x<threshold:
            table.append(0)
        else:
            table.append(1)
    image=image.point(table,'1')
    return image

def main():
    while(True):
        if time.strftime("%M", time.localtime(time.time())) == '00' or time.strftime("%M", time.localtime(time.time())) == '59':
            submitRequests()
            submitRequests()
            submitRequests()
            submitRequests()
            submitRequests()
            submitRequests()
                

def submitRequests():
    image = requests.get('http://dxyq.njust.edu.cn/image', cookies=cookies, headers = getImageHeaders, proxies=proxies)
    validateNum = getImageNumStr(image)
    validateNum = twiceCorrect(validateNum)
    params['validate'] = validateNum
    print(params)
    response = requests.post('http://dxyq.njust.edu.cn/ajax/orderSave.action', cookies=cookies, headers=headers, data=params, proxies=proxies)
    response.encoding = 'utf-8'
    content = json.loads(response.content)
    res = content['result']['result']
    message = content['result']['message']
    print('%s:  申请结果：%s,  信息：%s' % (time.strftime("%H:%M:%S", time.localtime(time.time())), res, message))
        
        
def twiceCorrect(src):
    return errorMap.get(src, src)
        
def getNextImageCount():
    baseImagePath = 'D:/images'
    imageFileNames = os.listdir(baseImagePath)
    pattern = re.compile('(\d+)\.jpg')
    maxNum = -1
    for imageFile in imageFileNames:
        match = re.findall(pattern, imageFile)
        #print(imageFile)
        num = int(match[0])
        if num > maxNum:
            maxNum = num
    return maxNum + 1
    
def transHundersImages():
    basePath = 'D:/images/%d.jpg'
    errorCount = 0
    errorList = []
    errorRes = []
    for i in range(1, 350):
        imagePath = basePath % (i)
        if not os.path.exists(imagePath):
            continue
        image = binaryzation(141, imagePath)
        result = pytesseract.image_to_string(image)
        result = twiceCorrect(result)
        print('%-5dresult: %s' % (i, result))
        if len(result) != 4 or not result.isdigit():
            errorCount += 1
            image.show()
            errorList.append(i)
            errorRes.append(result)
    print('错误个数为： %d' % (errorCount))
    print('错误的图为：', errorList)
    print('错误的结果为：', errorRes)
    

def getImageNumStr(response):
    image = response.content
    num =getNextImageCount()
    path = 'D:/images/%d.jpg' % num
    with open(path, 'wb') as f:
        f.write(image)
    image=binaryzation(141, path)
    result=pytesseract.image_to_string(image)
    print('图片写入D:/images成功，路径为%s, 识别图片验证码为%s' % (path, result))
    return result
    
#main()
#transHundersImages()
#getNextImageCount()


# In[130]:


main()


# In[7]:


#'D:/images/%d.jpg' % 3


# In[19]:


#os.listdir('D:/images')


# In[27]:


#[random.randint(0, 100) for i in range(20)]


# In[119]:


#pattern = 'D:/images/(\d+)\.jpg'
#result = re.findall(pattern, 'D:/images/311.jpg')
#result[0]


# In[69]:


#image = requests.get('http://dxyq.njust.edu.cn/image', cookies=cookies, headers = getImageHeaders, proxies=proxies)
#getImagePath(image)


# In[67]:


#result = requests.get('http://www.baidu.com', verify = False)
#result.encoding = 'utf-8'
#result.status_code


# In[102]:


#'12f0'.isdigit()

