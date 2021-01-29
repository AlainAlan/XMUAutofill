from selenium import webdriver
import time
import sys


logfile = 'log.txt' #打印日志文件的地址，可以随意修改
logarchive = 'logarchive.txt'
userfile = 'users'  #存放用户名密码的文件地址，可以随意修改
url = 'https://xmuxg.xmu.edu.cn/login'
chromedriver = 'C:/chromedriver.exe' #修改此处路径为你放置chromedriver.exe的位置
go_to_daka = True


def daka(a, b):
	'''去打卡'''
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
		save = driver.find_element_by_xpath("//*[@class='preview-container']/div[1]/div[1]/span[1]/span[1]")
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

with open(userfile, 'r', encoding='UTF-8') as users:
	today_date = (time.strftime('%Y_%m_%d', time.localtime(time.time())))
	lines = users.readlines()
	for line in lines:
		line = line.strip()
		if line[0] == '#':
			continue
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
						if datetime_and_output[4].strip() not in ["已打卡", "打卡成功"]:
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
			renewing_log.write(cur_time + " " + a + " 旧的日志已被归档在" + logarchive + "内\n")
			renewing_log.close()

		with open(logfile, 'a', encoding='UTF-8') as log:
			log.write(cur_time + ' ' + a + ' ' + output + '\n')
			print("记录日志")

		print('End\n')