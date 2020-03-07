#-*- coding:utf-8 -*-
import urllib2
import re
for idnum in xrange(102,130):
    headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Mobile Safari/537.36"}
    url = "http://www.qddlys.com/NewsDetail.aspx?ID="+str(idnum)
    try:
        req = urllib2.Request(url,data=None,headers=headers)
        response = urllib2.urlopen(req)
        html = response.read()
        pat = re.compile(r'id="lblContent".*?<strong.*?>(.+)</strong>.*?(\d{17}[\w\d])')
        mat = re.search(pat,html)
        f = open("name.txt","a+")
        f.write(mat.groups()[0]+'\t')
        f.write(mat.groups()[1]+'\r\n')
        f.close()
    except Exception:
        continue

