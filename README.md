###官方发布点   https://github.com/zogvm/zogud
###zogna 自动更新程序 
####使用说明:
#####在 本地应用 端：

* 拷贝 zogud.exe 和 python34.dll 和 version文件 到程序目录下
* version为文本格式， 里面下一个待更新的版本号，只能为整数。初始化可以写1

####在 更新服务 端：

* 假设 当前服务器地址:  http://127.0.0.1:8080
* 在目录下新建 topnew.txt 为文本格式， 里面为最新的版本号，只能整数。如 1
* 在目录下新建 版本号的文件夹， 如 /1/
* 在/1/里 新建 version.txt 为文本格式，里面为当更新完1以后的下一个版本号。如 2
* 在/1/里 新建 updatelist.txt 为文本格式，里面写 要更新的文件表

* 标准格式为(无需带引号分割 全部用TAB键分割)

	-符号TAB源路径TAB目的路径

	-其中符号 为 * :新增 一个目录
		 为 / :删除 一个目录
		 为 + :新增或替换 一个文件
		 为 - :删除 一个文件
	-其中 源路径	为 下载源的相对路径:如 http://127.0.0.1:8080/1/version.txt，则填写version.txt即可
	-其中 目的路径	为 程序本地的相对路径:如 D:/zogud.exe 则 填写zogud.exe


####zogud 用法

	-h [无参]帮助
	-s 源地址 URL 必填
	-d 目的地址 本地 必填
	-p http://user:password@192.168.1.1:8000/  代理 可以不设
	-m http https 代理模式(GITHUB用HTTPS) 可以不设
	-u 1 更新模式：1-逐级更新 2-跳级更新 默认为1
	-w 1 休息时间 秒 可以不设
	-t 10 超时设定 秒 默认10秒 可以不设

#####举例：
* 如更新服务器 http://127.0.0.1:8080/1/version.txt
* 如本地程序路径 d:/program/a/zogud.exe
* zogud.exe -s http://127.0.0.1:8080 -e 'd:/program/a/'




