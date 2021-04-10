##### 附识

玩意儿是大佬搞的（readme只佛头着粪，不敢擅动）——不好意思一不小心就fork了，本来寻思只动动针黹打个补丁来着。正常人不会自带服务器的（no offense），故而还是着重于Windows任务计划程序（Windows chauvinist就是我）。思路如下：
1. 每次打开电脑时自动运行
2. 为了避免每次打开电脑都实际登录，先读取日志看看是否已经打卡
3. 为了避免日志又臭又长，当日志超过一定长度自动归档日志

一些小的更改：
1. 指定UTF8编码，因为在某些机器上报错了。
2. 怂，sleep就久了一些，稳如狗，妥当如**郑妥娘**。
###### 配置教程

众所周知，都用Linux了就不需要教程了。以下仅针对Windows用户。<br>

* 【Windows】 一般人已经有了 <br>
* 【Chrome】 没有就去下<br>
* 【[chromedriver](http://npm.taobao.org/mirrors/chromedriver/)】 <br>

```
# windows 查找chrome版本,在浏览器地址栏中输入
chrome://version

# 然后点击上述链接，下载对应版本，若无法版本号最后的数字无法对应，下载最接近的即可。

# 将exe解压到你喜欢的路径（并将路径填到py文件的开头对应位置）
# 没有更好的编辑器可以使用记事本打开py文件

```
* 【Python】 问百度，很简单就能装好
* 【Selenium】
打开PowerShell（找不到可以搜索，或者在某文件夹下Shift+空白处右键点击，运行PowerShell），输入：
```
pip3 install selenium
```
用记事本打开user，填入自己的账号和密码，替代原有的示例。

关于任务计划程序，请参考：<br>
[python脚本在Windows计划任务执行问题_ChenZhuYuの小屋-CSDN博客](https://blog.csdn.net/chenzhuyu/article/details/50363873)
> 最近在添加计划任务时py脚本总不能正确执行，最后终于找到了，感谢伟大的Google，但是和原博主一样不知道为什么，以后慢慢再解决吧。解决方案如下：只需要在创建任务中的“操作”选项卡里面，新建操作， **“程序或脚本”** 中只填脚本名称[fill.py]，在 **“起始于”** 里面填写脚本所在的路径[e.g.: C:/fill.py]。保存，生效！。。。
触发器建议设置为：所有账户登录后+延迟一分钟（等待网络连接好）运行。

###### 个人建议

- 不建议服务器自动打卡，万一人没了健康打卡还在自动运行就不好了。
- 这意味着：每次打卡程序运行之前你都确认了自己的健康状况，程序仅仅自动化了打卡过程而已。（开脱罪名）
- 如果龙体欠安，建议在运行之初即叉掉程序，或者及时更新健康状况。
- 建议只给自己打卡，但是保留了原来多人打卡的功能，但不曾测试。

###### 还没搞的
- [x] 根据时间判断是否到了打卡时间，否则如笔者这样的夜猫子凌晨开机也会尝试打卡
- [x] 2021.3.27增加了邮件推送功能，具体建议百度。如果不需要可以注释掉相应代码行。
- [ ] 提高耐（鲁）操（棒）性，user文件如果没按规则填写split出的列表长度不恰等于**二**就翘辫子的程序是不行的
- [ ] 如果在认证服务的设置中设置了仅允许一个设备登录，则会被跳转到一个登出其他设备的页面，程序还无法处理这种情况，只能修改设置<br>
- [x] 自动发邮箱
- [ ] webvpn（已本地实现，没更新）

###### 更新

- 2021-04-10：更新了保存按钮的xpath



# Xiamen University automatic daily health check in 
自从用了这个，辅导员再也不用催我打卡了。腰也不酸了，腿也不疼了，注意力也更集中了，我感觉我又行了。<br>
最好在服务器等永不关机的环境下运行，否则失去了自动的意义<br>
users文件中可添加多个账号密码，打卡结果会记录在log.txt中<br>

## Environment
* Linux/windows <br>
* chrome <br>
* [chromedriver](http://npm.taobao.org/mirrors/chromedriver/) <br>
```
# linux 查找chrome版本，在命令行中输入
google-chrome -version

# windows 查找chrome版本,在浏览器地址栏中输入
chrome://version

# 然后点击上述链接，下载对应版本，若无法版本号最后的数字无法对应，下载最接近的即可。
# windows 可放在chrome的安装位置，例如
c:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe
# ubuntu 拷贝至
/usr/bin/chromedriver
```

* python 3.6+ <br>

## Python lib
selenium <br>
```
pip3 install selenium
```
## Linux
* 直接运行
```
bash fill.sh 
```

* 编辑定时脚本
```
crontab -l //查看系统中已有的定时任务
crontab -e //编辑定时任务
```

* 定时脚本样例
```
crontab -e
4 9 * * * bash /your/path/to/fill.sh #每天9点4分自动执行任
0 11 * * * bash /your/path/to/fill.sh #每天11点0分自动执行任务
```

## Windwos
```
python3 fill.py
```
## TO DO
- [x] 打印日志 <br>
- [ ] 自动发送结果到指定邮箱 <br>
- [ ] 与微信结合<br>
- [ ] Windows脚本<br>
- [ ] Mac版<br>
- [ ] 账号密码加密传输<br>

## 更新日志
2020.12.11 更新查找登录按钮
```
driver.find_element_by_xpath("//*[@class='auth_login_btn primary full_width']").click() #登录
```
## License

This project is released under the [GNU GPL v3.0](LICENSE).
