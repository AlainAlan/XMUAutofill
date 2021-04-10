from selenium import webdriver
import time
from datetime import datetime
import os
import msvcrt
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import random

logfile = 'log.txt' #打印日志文件的地址，可以随意修改
logarchive = 'logarchive.txt'
userfile = 'users'  #存放用户名密码的文件地址，可以随意修改
url = 'https://xmuxg.xmu.edu.cn/login'
chromedriver = 'C:/chromedriver.exe' #修改此处路径为你放置chromedriver.exe的位置

def send_mail(content):
	'''
	https://zhuanlan.zhihu.com/p/89868804
	下面的中文内容需要自己调整
	'''
	mail_host = "smtp.126.com"
	mail_sender = "发送@126.com"
	mail_license = "从邮箱设置配置后复制"
	mail_receivers = ["接收@qq.com"]
	subject_content = content
	mm = MIMEMultipart('related')
	mm["From"] = "DailyHealthReport<发送@126.com>"
	mm["To"] = "Name<接收@qq.com>"
	mm["Subject"] = Header(subject_content,'utf-8')
	# 下面用于配置邮件的内容
	# qieyun.txt是三百多个常用字在《广韵》中的音韵地位
	# 可以搞成自己喜欢的东西
	with open('qieyun.txt','r', encoding='UTF-8') as a:
		lines = a.readlines()
		line = random.choice(lines)
	body_content = line
	message_text = MIMEText(body_content,"plain","utf-8")
	mm.attach(message_text)
	stp = smtplib.SMTP()
	stp.connect(mail_host, 25)  
	stp.set_debuglevel(1)
	stp.login(mail_sender,mail_license)
	stp.sendmail(mail_sender, mail_receivers, mm.as_string())
	print("邮件发送成功")
	stp.quit()

def getInput(timeout = 20):
	# https://blog.csdn.net/weixin_38604589/article/details/89295922
	start_time = time.time()
	input = ''
	while True:
		if msvcrt.kbhit():
			# https://blog.csdn.net/zyl_wjl_1413/article/details/84864482
			input = msvcrt.getche()
		if len(input) != 0 or (time.time() - start_time) > timeout:
			break
	if len(input) > 0:
		# print(str(input))
		return str(input)
	else:
		return "超时"

def zhen_daka(a, b):

	driver = webdriver.Chrome(chromedriver)
	run = True
	now = time.time()

	while run:
		try:
			driver.get(url)
			break
		except:
			print(url, "获取失败，重试中")
			if (time.time() - now) > 10:
				run = False
				return '网页登陆失败'

	driver.maximize_window()
	# logintab = driver.find_element_by_class_name('login-tab')
	login = driver.find_element_by_xpath("//*[@class='buttonBox']/button[2]")
	login.click()

	time.sleep(3)
	c = driver.find_element_by_id('username')
	d = driver.find_element_by_id('password')
	c.send_keys(a)
	d.send_keys(b)

	#driver.find_element_by_xpath("//*[@id='casLoginForm']/p[4]").click() #登录
	driver.find_element_by_xpath("//*[@class='auth_login_btn primary full_width']").click() #登录
	driver.get('https://xmuxg.xmu.edu.cn/app/214')

	now = time.time()
	while True:
		try:
			form = driver.find_element_by_xpath("//*[@class='gm-scroll-view']/div[2]") #我的表单
			form.click()
			break
		except:
			time.sleep(2)
			print("获取\"我的表单\"失败，重试中")
			if (time.time() - now) > 10:
				run = False
				return '获取\"我的表单\"失败'

	now = time.time()
	while True :
		try:
			text = driver.find_element_by_xpath("//*[@id='select_1582538939790']/div[1]/div[1]/span[1]").text
			break
		except:
			time.sleep(3)
			print("查找框内文本失败，重试中")
			if (time.time() - now) > 10:
				run = False
				return '查找框内文本失败'
	
	if text == '请选择':
		now = time.time()
		while True:
			try:
				yes = driver.find_element_by_xpath("//*[@id='select_1582538939790']/div[1]/div[1]") #定位填“是”的页面
				yes.click()
				break
			except:
				time.sleep(2)
				print("点击\"是\"失败，重试中")
				if (time.time() - now) > 10:
					run = False
					return '点击\"是\"失败'

		now = time.time()
		while True:
			try:
				yes = driver.find_element_by_xpath("//*[@class='v-select-cover']/ul[1]/div[1]")
				yes.click()
				break
			except:
				time.sleep(2)
				print("确认\"是\"失败，重试中")
				if (time.time() - now) > 10:
					return '确认\"是\"失败'
		# save = driver.find_element_by_xpath("//*[@class='preview-container']/div[1]/div[1]/span[1]/span[1]")
		save = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/span/span")
		save.click()

		time.sleep(1)
		driver.switch_to_alert().accept() # 保存确定
		time.sleep(2)
		output = '打卡成功'
	elif text == '是 Yes':
		output = '已打卡'
	else:
		output = '打卡失败！！！'
	driver.close()
	return output

def daka(a, b):
	'''去打卡'''

	# 范围时间
	open_time = datetime.strptime(str(datetime.now().date())+'7:00', '%Y-%m-%d%H:%M')
	close_time = datetime.strptime(str(datetime.now().date())+'19:30', '%Y-%m-%d%H:%M')
	 
	# 当前时间
	now_time = datetime.now()
	
	if now_time < open_time:
		print("你今天怎么起那么早，还是说还没睡？？\n还不到打卡时间，你记得七点之后打卡")
		time.sleep(5)
		output = "时辰未到"

	elif now_time > close_time:
		print("已经过了打卡时间了。你确定今天系统又出毛病了？")
		print("如果确定系统还没关闭请输入1\n")
		maobing = getInput()
		if maobing == "b'1'":
			output = zhen_daka(a,b)
		elif maobing == "超时":
			output = "吉时已过且反应超时"
		else:
			output = "风太大我没听清"
	else:
		output = zhen_daka(a,b)
	
	return output

with open(userfile, 'r', encoding='UTF-8') as users:
	today_date = (time.strftime('%Y_%m_%d', time.localtime(time.time())))
	lines = users.readlines()
	for line in lines:
		line = line.strip()
		if line[0] == '#':
			continue
		
		go_to_daka = True

		a, b = line.split(' ')
		# 是否清空日志
		renew_log = False
		# 检查打卡记录
		with open(logfile, 'r', encoding='UTF-8') as logs:
			log_lines = logs.readlines()
			log_lines_num = len(log_lines)
			if log_lines_num > 10:
				renew_log = True
			for log_line in log_lines:
				datetime_and_output = log_line.split(' ')
				date = datetime_and_output[0]
				if date != today_date:
					print("不是这天。")
					continue
				else:
					if datetime_and_output[3].strip() != a:
						print("不是这人。")
						continue
					else:
						if datetime_and_output[4].strip() not in ["已打卡", "打卡成功", "日志显示已打卡"]:
							print("这人还没打卡。")
							continue
						else:
							print("这人打过卡了。")
							output = "日志显示已打卡"
							go_to_daka = False
							break

		if go_to_daka == True:
			output = daka(a, b)
		cur_time = (time.strftime('%Y_%m_%d %r', time.localtime(time.time())))
		# 如果日志文件过大
		if renew_log:
			file_to_archive = open(logfile, 'r', encoding='UTF-8')
			log_to_archive = file_to_archive.read()

			where_log_archive = open(logarchive,'a', encoding='UTF-8')
			where_log_archive.write(log_to_archive)

			file_to_archive.close()
			where_log_archive.close()

			# 写入新日志
			renewing_log = open(logfile, 'w', encoding='UTF-8')
			renewing_log.write(cur_time + " " + a + " 旧的日志已被归档\n")
			renewing_log.close()

		with open(logfile, 'a', encoding='UTF-8') as log:
			log.write(cur_time + ' ' + a + ' ' + output + '\n')
			print("记录日志")
		# 如果不想配置邮件发送功能，用“#”注释掉下面几行即可
		# 如果只想在打卡失败时接收邮件，可以把下面的列表改成['已打卡','日志显示已打卡','打卡成功']
		# 这样将会忽略打卡成功
		if output not in ['已打卡','日志显示已打卡']:
			send_mail(output)
			print('已发送邮件')
		# send_mail(output)
		# 取消注释上面这一行（而注释掉前面几行），可以无条件发送邮件
		
		
		print('End\n')
