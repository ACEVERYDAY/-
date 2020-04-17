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
