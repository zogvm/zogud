#!/usr/bin/env python
# -*- coding: utf-8 -*-

from DownLoad import Download_Get
import time
import sys,getopt
import os
import shutil

#更新标志


# TOMCAT服务器要建立
# \update 文件夹
# 里面topnew.txt 为最新版本号
# topnew=N 设 Update/N/version.txt =N+1 设本机version.txt=N 此时 版本要 curVer > TopNew 才不更新 相等也要更新。
# \update\N\ 为要从N版本升级到M版本的 文件夹
# \update\N\updatelist.txt 为更新列表
# \update\N\version.txt 为本次升级到M版本的版本号
#
# 本机目录下要有yrversion.txt 为当前版本号
# //UPDALIST里面以 TAB来隔开，路径不要含有空格，
# 如以下
# * ODAC ODAC		//新建文件夹
# / ODAC ODAC		//删除文件夹
# + ODAC/b.txt ODAC\b.txt	//新建文件
# - a.txt   a.txt			//删除文件
# + version.txt version.txt	//新建文件 下一版本


#读取版本文件
def ReadCurV(path):
    print(path)
    try:
        fw = open(path, 'rb')
    except Exception as e:
        print("错误：无法打开 %s" % path)
        sys.exit()
    a=fw.readline().strip()
    fw.close()

    if len(a) == 0:
        print("错误：没有版本号")
        sys.exit()
    return int(a)

#读取更新文件
def ReadUpList(path):
    try:
        fw = open(path, 'r')
    except Exception as e:
        print("错误：无法打开 %s" % path)
        sys.exit()

    uplist=[]
    for line in fw:
        line=line.strip()
        if len(line) >0:
            uplist.append(line.split('\t'))
    fw.close()
    return uplist


def  usage():
    print("-h [无参]帮助")
    print("-s 源地址 URL 必填")
    print("-d 目的地址 本地 默认为当前路径 可以不设")
    print("-p http://user:password@192.168.1.1:8000/  代理 可以不设")
    print("-m http https 代理模式(GITHUB用HTTPS) 可以不设")
    print("-u 1 更新模式：1-逐版本更新 2-跳到最新版本进行更新 默认为1 可以不设")
    print("-w 1 休息时间 秒 可以不设")
    print("-t 10 超时设定 秒 默认10秒 可以不设")

if __name__ == '__main__':

    proxyip=""
    proxymode=""
    waittime=0.1
    timeoutS=10
    src_addr=""
    if len(os.path.split(sys.argv[0])[0]) >0:
        dst_addr=os.path.split(sys.argv[0])[0]
        dst_temp=os.path.split(sys.argv[0])[0]+"/zogud_temp/"
    else:
        dst_addr="."
        dst_temp="./zogud_temp/"

    updateJumpMode=False
    myheaders = {'User-Agent': 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25'}

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:d:p:m:u:w:t:")
        for op, value in opts:
            if op == "-h":
                usage()
                sys.exit()
            elif op == "-s":
                src_addr=value
            elif op == "-d":
                dst_addr=value
                dst_temp=value+"/zogud_temp/"
            elif op == "-p":
                proxyip= value
            elif op == "-m":
                proxymode= value
            elif op == "-u":
                if value == '1':
                    updateJumpMode=False
                else:
                    updateJumpMode=True
            elif op == "-w":
                waittime=int(value)
            elif op == "-t":
                timeoutS=int(value)
            else:
                usage()
                sys.exit()
    except Exception as e:
        usage()
        sys.exit()

    if  len(src_addr) == 0 :
        print("-s 源地址 未填")
        sys.exit()

    proxys={proxymode,proxyip}

    #开始咯
    #删除 与创建

    shutil.rmtree(dst_temp,True)
    os.makedirs(dst_temp,exist_ok=True)

    if len(proxyip)>0:
        Download_Get(src_addr+"/topnew.txt",dst_temp+"/topnew.txt",timeout=timeoutS,proxies=proxys,headers=myheaders,verify=False)
    else:
        Download_Get(src_addr+"/topnew.txt",dst_temp+"/topnew.txt",timeout=timeoutS,headers=myheaders,verify=False)

    FinalVersion=ReadCurV(dst_temp+"/topnew.txt")

    while 1:
        CurVersion=ReadCurV(dst_addr+"/version")
        print("准备更新到"+str(CurVersion))
        if  CurVersion > FinalVersion :
            break

        if updateJumpMode:
            NextVersion=FinalVersion
        else:
            NextVersion=CurVersion

        #准备下载
        if len(proxyip)>0:
            Download_Get(src_addr+"/"+str(NextVersion)+"/updatelist.txt",dst_temp+"/updatelist.txt",timeout=timeoutS,proxies=proxys,headers=myheaders,verify=False)
        else:
            Download_Get(src_addr+"/"+str(NextVersion)+"/updatelist.txt",dst_temp+"/updatelist.txt",timeout=timeoutS,headers=myheaders,verify=False)

        uplist=ReadUpList(dst_temp+"/updatelist.txt")
        for c,src,dst in uplist:
            if c == '*':
                os.makedirs(dst_addr+"/"+dst+"/",exist_ok=True)
                os.makedirs(dst_temp+"/"+dst+"/",exist_ok=True)
            elif c == '+':
                if len(proxyip)>0:
                    Download_Get(src_addr+"/"+str(NextVersion)+"/"+src,dst_temp+"/"+dst,timeout=timeoutS,proxies=proxys,headers=myheaders,verify=False)
                else:
                    Download_Get(src_addr+"/"+str(NextVersion)+"/"+src,dst_temp+"/"+dst,timeout=timeoutS,headers=myheaders,verify=False)

                time.sleep(waittime)

            #是自己 复制下然后退出
            if  dst == os.path.split(sys.argv[0])[1]:
                newpath= os.path.splitext(sys.argv[0])[0]+"_old.exe"
                shutil.copy(sys.argv[0],newpath)
                #不加START无法异步
                newargv="start "+newpath+" "
                for ar in sys.argv[1:]:
                    newargv+=ar+" "
                os.system(newargv)
                print("自退出")
                sys.exit()

        #下载完了 准备拷贝
        for c,src,dst in uplist:
            if c == '+':
                shutil.copy(dst_temp+"/"+dst,dst_addr+"/"+dst)
            elif  c == '/':
                shutil.rmtree(dst_addr+"/"+dst+"/",True)
            elif c == '-':
                try:
                    os.remove(dst_addr+"/"+dst)
                except Exception as e:
                    pass

    shutil.rmtree(dst_temp,True)

    print("更新完毕")

