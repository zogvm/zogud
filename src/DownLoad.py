#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys

def Download_Get(url,path, **kwargs):
    # print("arg:", args)
    print("下载:",url,"到:",path)
    session=requests.session();
    # for key in kwargs:
    #     print("kwargs %s: %s" % (key, kwargs[key]))
    try:
        req = session.get(url,**kwargs)
        print('Status:',req.status_code, req.raise_for_status())
    except requests.exceptions.HTTPError as e:
        print('requests.exceptions.HTTPError:',e)
        print("网络错误")
        sys.exit()
    except requests.exceptions.Timeout as e:
        print('requests.exceptions.Timeout:',e)
        print("网络错误")
        sys.exit()
    except requests.exceptions.ConnectionError as e:
        print('requests.exceptions.ConnectionError:',e)
        print("网络错误")
        sys.exit()
    except requests.exceptions.TooManyRedirects as e:
        print('requests.exceptions.TooManyRedirects:',e)
        print("网络错误")
        sys.exit()
    except requests.exceptions.RequestException as e:
        print('requests.exceptions.RequestException:',e)
        print("网络错误")
        sys.exit()
    except Exception as e:
        print("HTTPConnection no:"+e)
        print("网络错误")
        sys.exit()

    #print('headers:',req.headers)
    #req.encoding = 'utf-8'
    #print('Data:', html_str)
    fw = open(path, 'wb')
    fw.write(req.content)
    fw.close()
