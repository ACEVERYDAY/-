疫情期间身体状况自动填报脚本
An Auto-Tool for Reporting of physical condition during epidemic
@[TOC](文章目录)
## 前言
因为疫情缘故，学校搞了个每日限时打卡的系统，要求学生在每天0-9点完成当日体温和在京状况的打卡。就这样手动打卡了两个多月，北京还是迟迟不开学，目测开学已经要到5月底了。打卡期间忘过无数次，每次都被班长提醒，学校还往家长手机里发送作者没有打卡的短信，神烦。
于是乎，决定使用 定时开关机软件 + python 实现一个全自动定时打卡的脚本，省却我接下来一个月的劳神费力。
学校的打卡系统登录界面是这样的：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200417103553364.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NwcmltZXNwbHVz,size_16,color_FFFFFF,t_70)
这里是填写界面（左侧菜单栏需要依次点击数据采集和学生每日上报才能出现表格，否则是空白页面。表格很长，注意有纵向和横向滚动条）
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200417103902118.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NwcmltZXNwbHVz,size_16,color_FFFFFF,t_70)
***

## 问题分析
手动操作时的步骤是这样的：
进入学生登录界面-->输入账号密码
-->进入填报界面-->点击左侧菜单栏-->点击数据采集-->点击学生每日上报
-->进入表格-->点击表格左下角“与昨日情况一致”
-->手动填写当日体温-->滑动横向滚动条-->手动填写当日在京情况(一直在京)

因此在使用selenium时，其大致步骤与上面描述的无二。
***
## 网页源码分析与代码实现
### 一、加载火狐驱动
selenium需要模拟打开浏览器，这里一般使用的浏览器驱动(Driver)是谷歌或者火狐，笔者先尝试了谷歌的驱动，发现在源码分析的时候效果不是很理想，于是用了火狐的。
（关于驱动的下载与安装，这里不做赘述，百度即可查看。）
驱动加载并进入后，脚本会自动根据当前的驱动打开对应的火狐浏览器，并链接到提供url的网页。

```python
driver = webdriver.Firefox()  # 利用火狐浏览器
# 填写疫情上报系统的url
url = r"http://tb.bucea.edu.cn:8075/WebReport/ReportServer?op\=fs_load&cmd=fs_signin&_=1586929099201"
driver.get(url)
# 最大化浏览器窗体
driver.maximize_window()
```
### 二、输入账号密码并提交
想要实现填写指定数据并自动填写到对应的位置，或者点击按钮提交到对应位置，就需要通过网页的各种标签的`id`或者`class`来定位相对应的元素，学过web编程的同学应该比较好理解这点。
例如下面这段用于填写用户名的代码

```html
<div class="fs-login-input fs-login-input-username">
    <input tabindex="1" class="fs-login-username" type="text" placeholder="用户名" title="用户名">
</div>
```
我们可以看到，这部分的核心在于`<input>`标签，此标签没有指定`id`，而是给了`class`，因此可以使用selenium提供的`driver.find_element_by_class_name()`方法，通过`class`的值来定位元素，进而调用`send_keys()`方法来实现数据填充。
类似的，对于“点击”操作，只需要获取`<button>`或`<radio>`或`<a>`标签的class或者id，进而调用`onclick()`方法达到点击目的。
关于如何定位元素，可以参考这篇文章[《史上最全！Selenium元素定位的30种方式》](https://blog.csdn.net/qq_32897143/article/details/80383502)
笔记本上使用Fn+F12可以启用源代码查看器，点击页面中某个部分，便能自动锁定相应代码，非常好用。我们的页面是下图这样的，因此可以通过这段代码来定位“输入用户名”这个元素并设置数据：

```python
elem = driver.find_element_by_class_name('fs-login-username')
elem.send_keys(stu_number)
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200417111148506.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NwcmltZXNwbHVz,size_16,color_FFFFFF,t_70)

```python
# 疫情打卡系统url
url = r"http://tb.bucea.edu.cn:8075/WebReport/ReportServer?op=fs_load&cmd=fs_signin&_=1586929099201"
driver.get(url)
driver.maximize_window()
# 填写用户名和密码
elem = driver.find_element_by_class_name('fs-login-username')
elem.send_keys(stu_number)
elem = driver.find_element_by_class_name('fs-login-password')
elem.send_keys(stu_password)
# 提交表单
driver.find_element_by_xpath("//*[@id='fs-login-btn']").click()
```

### 三、进入打卡界面并点击左侧菜单栏
点击提交且用户验证成功后，会跳转到另外一个url，这个界面用于填写当日身体情况。依次点击左侧菜单栏的数据采集->学生每日上报，可以进入表格界面，如图：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200417103902118.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NwcmltZXNwbHVz,size_16,color_FFFFFF,t_70)在第二节的分析中，笔者已经确定了定位元素的基本流程，按照selenium给定的方法，便可依次点开左侧菜单栏（这里每执行一步后，尽量使用`time.sleep()`让程序休息一小段时间，否则页面可能会卡住或者代码执行无效）。
**但是！** 随之而来的是困扰了我一天的地方。想要定位表格窗体的元素时，却怎么都定位不到，我试了好多地方，发现只有表格窗体中的元素是无法定位的。

#### iframe内元素的定位

学过web的同学知道，这种页面的header和菜单栏基本是固定的，通过内嵌`<iframe>`或者`<frame>`的方式，可以达到不同页面在相同url中切换、而指定部分（例如菜单栏 表头等）不变的目的。
于是我猜测元素定位不到可能与`<iframe>`的引入有关，也就是说，菜单栏和表格窗体构成的页面并非一个整体，而是两个模块的拼接。遂检索相关文章，发现果然如此。
如果页面使用了`<iframe>`，想要定位内嵌界面中的某个元素，在编写代码并调用selenium时，需要进入相应的`<iframe>`内！
知道了这点，就很容易解决了：Fn+F12查看页面源代码，把鼠标放在滚动条上就能查看到内嵌页面的`<iframe>`的id或者class，耐心网上翻一点，就能找到表格所在的iframe了：fs_tab_1587094181588
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020041711305412.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NwcmltZXNwbHVz,size_16,color_FFFFFF,t_70)
我兴冲冲的编写代码进入iframe并重启程序测试:

```python
driver.switch_to.frame(driver.find_element_by_xpath("fs_tab_1587094181588"))
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200417113353654.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NwcmltZXNwbHVz,size_16,color_FFFFFF,t_70)
#### 动态id/class的定位

**what？找不到iframe?**
不慌，盯着iframe的id`fs_tab_1587094181588`仔细思考了一下，后面一长串的数字像是动态生成的，而这种id一般前面的头部是不变的，即`fs_tab_`，于是我重新查看新页面的iframe的id，果然和上次打开的不一样了：fs_tab_1587094408952，表头也果然没变。
查看源码中以`fs_tab_`开头的id，发现只有一个，妙哉，可以使用了。
于是，通过`driver.find_element_by_xpath("//iframe[starts-with(@id, 'fs_tab_')]")`模糊匹配带有`fs_tab_`开头的id，并使用`driver.switch_to.frame()`进入相应的iframe，重新定位元素，成功了！

```python
# 由于是动态的id和class，因此... 
driver.switch_to.frame(driver.find_element_by_xpath("//iframe[starts-with(@id, 'fs_tab_')]"))
# 点击“与昨日情况一致”radio
driver.find_elements_by_class_name('fr-group-span')[0].click()
```

***
### 四、表格填写
经过上面这些分析后，下面的步骤就变得轻松多了。
由于每天填写的表格行数都是在动态变化的，比如今天的某个单元格id是D21-0-0，明天就变成了D-22-0-0，因此，对于获取当前日期应该填写的表格id，可以这样做：
根据日期差值与编写代码时的表格id相加，便得到了当日动态表格id

```python
def getDateDiff():
    # 2020-4-16编写，此时动态列数为21
    retire_day = datetime(2020, 4, 16)
    today = datetime.now()
    left_days = (retire_day - today).days  # 获取两个日期的天数差值
    return abs(left_days)

curColID = str(getDateDiff() + 20) + r'-0-0'
inputCol = ['D', 'AB']
```

点击“与昨日情况一致”后，还需要手动填写两个表格，分别是当日体温36度和“一直在京”，不怕，写个循环就搞定了：

```python
 # 列ID形式为：列编号-0-0
curColID = str(getDateDiff() + 20) + r'-0-0'
inputCol = ['D', 'AB']
inputVal = ['36', '一直在京']
for i in range(len(inputCol)):
	  inputBox = driver.find_element_by_id(inputCol[i] + curColID)
      driver.execute_script("arguments[0].scrollIntoView();", inputBox)
      time.sleep(1)
      # 开始模拟鼠标双击操作，不然无法锁定表格填数据
      action_chains = ActionChains(driver)
      action_chains.double_click(inputBox).perform()
      time.sleep(1)
      # 填写表格
      driver.find_element_by_xpath("//input[contains(@class,'fr-texteditor')]").send_keys(inputVal[i])
      time.sleep(1)
```

***
### 五、提交表格
一行代码：

```python
# css选择器选择button .x-emb-submit 这是关键
print(driver.find_element_by_css_selector('.x-emb-submit').click())
```

***
## 全部代码
奉上全部代码，有需要的同学可以参考：

```python
# encoding=utf8
import sys
import math
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

stu_number = '201706020115'
stu_password = '10200014'

# 获得日期差值，由于表格数据是动态变化的，可根据编写日期的行号和日期差来确定当日行号
def getDateDiff():
    # 2020-4-16编写，此时动态列数为21
    retire_day = datetime(2020, 4, 16)
    today = datetime.now()
    left_days = (retire_day - today).days  # 获取两个日期的天数差值
    return abs(left_days)

# 授权操作
def operationAuth(driver):

    try:
        # 疫情打卡系统url
        url = r"http://tb.bucea.edu.cn:8075/WebReport/ReportServer?op=fs_load&cmd=fs_signin&_=1586929099201"
        driver.get(url)
        driver.maximize_window()
        # 填写用户名和密码
        elem = driver.find_element_by_class_name('fs-login-username')
        elem.send_keys(stu_number)
        elem = driver.find_element_by_class_name('fs-login-password')
        elem.send_keys(stu_password)
        # 提交表单
        driver.find_element_by_xpath("//*[@id='fs-login-btn']").click()
        # 没有睡眠时间就不行switch_to.frame()
        time.sleep(2)
        # 模拟点击进入填报表格
        driver.find_element_by_link_text("数据采集").click()
        driver.find_element_by_link_text("学生每日上报").click()
        time.sleep(2)
        # 这地方写博客记录，由于是动态的id和class，因此...
        driver.switch_to.frame(driver.find_element_by_xpath("//iframe[starts-with(@id, 'fs_tab_')]"))
        # 点击“与昨日情况一致”radio
        driver.find_elements_by_class_name('fr-group-span')[0].click()

        # 列ID形式为：列编号-0-0
        curColID = str(getDateDiff() + 20) + r'-0-0'
        inputCol = ['D', 'AB']
        inputVal = ['36', '一直在京']
        for i in range(len(inputCol)):
            inputBox = driver.find_element_by_id(inputCol[i] + curColID)
            driver.execute_script("arguments[0].scrollIntoView();", inputBox)
            time.sleep(1)
            # 开始模拟鼠标双击操作，不然无法锁定表格填数据
            action_chains = ActionChains(driver)
            action_chains.double_click(inputBox).perform()
            time.sleep(1)
            # 填写体温度数
            driver.find_element_by_xpath("//input[contains(@class,'fr-texteditor')]").send_keys(inputVal[i])
            time.sleep(1)

        # css选择器选择button .x-emb-submit 这是关键
        print(driver.find_element_by_css_selector('.x-emb-submit').click())

    except TimeoutException:
        # 报错后就强制停止加载
        # 这里是js控制
        driver.execute_script('window.stop()')
        print(driver.page_source)

# 方法主入口
if __name__ == '__main__':
    # 加启动配置
    driver = webdriver.Firefox()  # 利用火狐浏览器
    # driver.get("http://www.baidu.com")  # 打开get到的网址
    operationAuth(driver)

```

