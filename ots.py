#-*- coding:utf-8 -*-
#!/usr/bin/env python

import urllib2,os,cookielib,urllib
import base64

import json,time,re

class RenRenRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_301( self, req, fp, code, msg, headers)
        result.status = code
        return result

    def http_error_302(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
        result.status = code
        return result

def get_url(opener,url,fname=None):
    req = urllib2.Request(url)
    
    res = opener.open(req).read()
    if fname:
        f=open(fname,'w+')
        f.write(res)
        f.close()
    return res

def post_url(opener,url,data,debug=False):
 #   if not debug:
  #      data = urllib.urlencode(dict([k, v.encode('utf-8')] for k, v in data.items()))
  #  print data
    req = urllib2.Request(url,urllib.urlencode(data))
    return opener.open(req).read()

def test():
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),RenRenRedirectHandler)
    url = 'https://kyfw.12306.cn/otn/login/init'
    res = get_url(opener,url,'/tmp/login.html')
    url = 'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand'
    
    get_url(opener,url,'/tmp/code.gif')

    url = 'https://kyfw.12306.cn/otn/passcodeNew/checkRandCodeAnsyn'
    code = raw_input("Input code")
    data = {
        'randCode':str(code),
        'rand':'sjrand'
    }
    
    post_url(opener,url,data)

    url = 'https://kyfw.12306.cn/otn/login/loginAysnSuggest'
    data = {
        'loginUserDTO.user_name':'XXX',
        'userDTO.password':'XXX',
        'randCode':code
    }
    #print '登陆请求'
    post_url(opener,url,data)

    url = 'https://kyfw.12306.cn/otn/login/userLogin'
    data = {
        '_json_att':''
    }
    print '登陆后的结果是'
    post_url(opener,url,data)
    
    time.sleep(1)
    url = 'https://kyfw.12306.cn/otn/leftTicket/init'
    get_url(opener,url)
    time.sleep(0.45)
    url = 'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand'
    get_url(opener,url)
    
    
        
    time.sleep(1)
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2014-01-08&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=XAY&purpose_codes=ADULT'
    response = get_url(opener,url)
    print '查询请求'
    print response

    lefts = json.loads(response)
    res_str = ''
    from_station_name = u'北京'
    to_station_name = u'西安'
    ypinfo = ''
    for le in lefts['data']:
        if le['queryLeftNewDTO']['station_train_code'] == 'Z19':
            ypinfo = le['queryLeftNewDTO']['yp_info']
            res_str = le['secretStr']
    
    time.sleep(1)
    url = 'https://kyfw.12306.cn/otn/login/checkUser'
    data = {
        '_json_att':''
    }
    post_url(opener,url,data)
    
    url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
    
    data = {
        'secretStr':urllib.unquote(res_str),
        'train_date':'2014-01-08',
        'back_train_date':'2013-1-30',
        'tour_flag':'dc',
        'purpose_codes':'ADULT',
        'query_from_station_name':'北京',
        'query_to_station_name':'西安',
        'undefined':''
    }
    print urllib.urlencode(data)
    print '提交订单'
    print post_url(opener,url,data)
    
    time.sleep(1)
    url= 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
    data = {
        '_json_att':''
    }
    print '提交之后'
    res = post_url(opener,url,data)
    
    m = re.search(r'globalRepeatSubmitToken\s=\s\'(\w+)\'',res)
    token = m.groups()[0]
       
    url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
    data = {
        '_json_att':'',
        'REPEAT_SUBMIT_TOKEN':token
    }
    print post_url(opener,url,data)
    
    url = 'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=passenger&rand=randp'
    get_url(opener,code_url,'/tmp/code.gif')
    code = raw_input("Input code")
    
    url = 'https://kyfw.12306.cn/otn/passcodeNew/checkRandCodeAnsyn'
    data = {
        'randCode':code,
        'rand':'randp',
        '_json_att':'',
        'REPEAT_SUBMIT_TOKEN':token
    }
    print post_url(opener,url,data)
    
    url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
    data = {
        'cancel_flag':2,
        'bed_level_order_num':'000000000000000000000000000000',
        'passengerTicketStr':'4,0,1,XXX,1,XXXXXXXXXXXXXXXXxX,,N',
        'oldPassengerStr':'XXX,1,XXXXXXXXXXXXXXXX,1_',
        'tour_flag':'dc',
        'randCode':code,
        '_json_att':'',
        'REPEAT_SUBMIT_TOKEN':token
    }
    print post_url(opener,url,data)
    
    url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
    data = {
        'train_date':'Wed Jan 08 2014 00:00:00 GMT+0800 (CST)',
        'train_no':'2400000Z190D',
        'stationTrainCode':'Z19',
        'seatType':4,
        'fromStationTelecode':'BXP',
        'toStationTelecode':'XAY',
        'leftTicket':ypinfo,
        'purpose_codes':'00',
        '_json_att':'',
        'REPEAT_SUBMIT_TOKEN':token
    }
    print post_url(opener,url,data)

    url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
    data = {
        'passengerTicketStr':'4,0,1,XXX,1,XXXXXXXXXXX,,N',
        'oldPassengerStr':'XXX,1,XXXXXXXXXXXXXXX,1_',
        'randCode':code,
        'purpose_codes':'00',
        'key_check_isChange':'95328B182C695CD2B5C6B4057651785EC9455FA8BCBE5EE5DCEBD802',
        'leftTicketStr':ypinfo,
        'train_location':'P3',
        '_json_att':'',
        'REPEAT_SUBMIT_TOKEN':token
    }

if __name__ == '__main__':
    test()
