ftp文件传输服务器	: 使用threading线程模块、socket模块，编写的文件服务器 可上传与下载文件

log_package	: logging模块 ，记录日志 使用配置文件的格式定义日志格式，
		：使用方法	：在要记录日志的模块 先导入这个配置文件，使用logging使用配置，直接logging打印日志即可
udp_聊天室	：使用socket udp 完成的

在线词典		:框架采用	；MVC架构    
			服务端：dict_server.py（逻辑处理)C
			              dict_db.py（数据处理）M
			客户端：dict_client.py（视图处理）V
		:技术使用：pymysql 、hashlib（加密密码为MD5）、threading（多线程）

http_server	：框架采用 ：前后端 分开
			web_server 前端     web_frame 后端
		:技术使用：tcp的多线程  俩端传输通信数据使用 json数据

并发相关操作_框架代码：

	struct传输不同类型数据	： 使用struct模块，struct方法打包任意python中数据类型 然后传递 另一方通过struct解包方法

	进程池_队列_拷贝目录文件	： 使用进程池、队列 ，编写管理进程任务的进程池

	多线程、多进程并发服务器	：进程、线程模块 ，编写多进程多线程处理任务

	服务器接收http	: socket、select模块（io多路复用），编写的http文件服务器  使用浏览器访问网址即可查看内容

