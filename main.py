#-*- coding:utf-8 -*-
#!/usr/bin/env python

TRAIN_ID = 'id_asdasd'

if __name__ == "__main__":
  cj = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),RenRenRedirectHandler)
  get_url(opener,url,None)
  get_url(opener,code_url,'code.png')
  data = {}
  login_data = json.loads(post_url(opener,async_url,data))
  code = raw_input("输入验证码")
  post_url(opener,login_url,login_data)
  qs = get_url(opener,get_query)
  qs = qs[2:-1]
  ss = qs.split('<span')
  aa = ''
  bb = ''
  for s in ss:
      if s.find(TRAIN_ID)>-1:
          mm = s.split('#')
          aa = mm[-3]
          bb = mm[-2]
  time.sleep(1)
  
  data = {}
  #....
  post_url(opener,order_url,data)
  
