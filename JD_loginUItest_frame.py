#!/usr/bin/env python
# coding: utf-8
# @Author  : Mr.K
# @Software: PyCharm Community Edition
# @Time    : 2019/11/23 2:41
# @Description: #使用selenium实现浏览器模拟UI登录，配合unittest框架实现UI功能测试



import time
import unittest
from congfig import *
import HTMLTestReportCN
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class JD_TestCase(unittest.TestCase):#继承uniitest,按照unittest框架写的

    def setUp(self):
        """
        每个用例执行前的操作：
        设置参数，并打开浏览器
        注意：这个函数在每次使用用例时会自动调用，因此不需要在用例中再写一次
        :return:
        """
        chrome_options = Options()#实例化类
        if browser_not_open:#是否打开浏览器终端
            chrome_options.add_argument('--headless')#不打开浏览器终端

        chrome_diver_path = diver_path  # chrome浏览器驱动地址
        global browser
        browser = webdriver.Chrome(executable_path=chrome_diver_path,chrome_options=chrome_options)  # 声明浏览器
        login_url = target_url  # JD登录url
        browser.get(login_url)  # 打开浏览器
        time.sleep(1)


    def tearDown(self):#每个用例执行后的收尾操作
        """
        每个用例执行后的操作：
        关闭浏览器
        :return:
        """
        browser.close()
        print("测试完成")
        pass



    def success_judge(self,wait_time,conter_time):
        """
        循环检测登录是否成功
        :param wait_time: 单次等待时长s
        :param conter_time: 尝试次数
        :return: bool登录成功True，失败False
        """
        wait_login = WebDriverWait(browser,wait_time)  # 设置浏览器等待扫码时间
        counter = 0  # 计数器初始化，共计数3次
        # 循环判断扫码登录是否成功

        print("等待中，共等待%d次，每次%d秒" % (conter_time, wait_time))
        while 1:
            try:
                wait_login.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,#通过特征来判断是否登录成功
                                                    '#ttbar-login > div.dt.cw-icon > a'))
                )
                print("登录成功")  # 成功则在报告中写入”wechat登录测试成功“
                return True
                break
            except TimeoutException:
                counter += 1  # 失败则继续尝试，3次后如依旧失败则在报告中写入”超时“
                print("第%d次等待超时" % (counter))
                if (counter == conter_time):
                    print("3次超时，登录失败")
                    return False
                    break



    def test_account_login(self):#Done
        """
        测试点1：账密登录jd能否实现
        :return:
        """
        browser.find_element_by_link_text('账户登录').click()#一定要点击一下切换选项卡，不然无法交互
        account=browser.find_element_by_id('loginname')
        password=browser.find_element_by_id('nloginpwd')
        submit=browser.find_element_by_id('loginsubmit')
        print(submit)

        account.clear()#清除输入框
        password.clear()
        account.send_keys(cs_acount)#传送账密
        password.send_keys(cs_passwords)
        submit.click()#点击登录按钮

        flag=self.success_judge(3, 3)  # 循环检测3次，每次3s，等待滑块验证完成

        # 使用断言来判断测试是否成功，如果失败则以第二个参数为信息写入report
        self.assertTrue(flag,"登录失败！原因：滑块移动验证超时")




    def test_twodcode_login(self):#Done
        """
        测试点2：二维码登录jd能否实现
        :return:
        """
        browser.find_element_by_link_text('扫码登录').click()
        flag=self.success_judge(3, 3)  # 循环检测3次，每次3s
        self.assertTrue(flag, "登录失败！原因：扫码超时")#使用断言来判断测试是否成功，如果失败则以第二个参数为信息写入report



    def test_account_logon(self):#done完成了一部分功能,并不完全
        """
        测试点3：注册新用户能否实现
        :return:
        """
        browser.find_element_by_link_text('立即注册').click()#点击立即注册后跳出新页面

        flag=0
        windows = browser.current_window_handle  # 获取当前页面句柄
        time.sleep(2)#等待页面跳出
        all_handles = browser.window_handles  # 获取全部页面句柄
        for handle in all_handles:  # 遍历全部页面句柄
            if handle != windows:  # 判断条件
                browser.close()#切换到新页面前需要把旧的页面关掉
                browser.switch_to.window(handle)  # 切换到新页面

        #print(browser.page_source)
        press_button=browser.find_element_by_class_name("protocol-button")#找到"同意并继续按钮"
        press_button.click()#点击"同意并继续按钮"

        tele_num = browser.find_element_by_id("form-phone")#找到手机号码键入框
        tele_num.clear()
        tele_num.send_keys(cs_telenumber)  # 传送手机号码
        time.sleep(1)

        vertify_button = browser.find_element_by_class_name("form-item.form-item-getcode")#找到点击验证按钮
        vertify_button.click()#点击验证按钮

        time.sleep(3)#等待手工滑块验证

        #这里有bug,不能通过这种方法判断手机是否被注册过
        # if(browser.find_element_by_class_name("registerDialog.checkRegDialog")):#如果出现这一行,说明手机号已被注册
        #     flag=0
        # else:
        #     flag=1
        #
        # self.assertTrue(flag, "登录失败！原因:手机已被注册")
        #点击下一步还有后续操作...





    def test_wechat_login(self):#Done
        """
        测试点4：微信登录能否实现
        :return:
        """
        browser.find_element_by_link_text('微信').click()#点击进入微信登录模块
        #微信扫码登录测试
        flag=self.success_judge(3,3)#循环检测3次，每次3s
        self.assertTrue(flag, "登录失败！原因：扫码超时")#使用断言来判断测试是否成功，如果失败则以第二个参数为信息写入report



    def test_qqtwodcode_login(self):#Done
        """
        测试点5：QQ二维码登录能否实现
        :return:
        """
        browser.find_element_by_link_text('QQ').click()
        #QQ扫码登录测试
        flag=self.success_judge(3, 3)  # 循环检测3次，每次3s
        self.assertTrue(flag, "登录失败！原因：扫码超时")  # 使用断言来判断测试是否成功，如果失败则以第二个参数为信息写入report



    def test_qqaccount_login(self):#Done
        """
        测试点6：QQ账密登录能否实现
        :return:
        """
        browser.find_element_by_link_text('QQ').click()
        time.sleep(1)

        iframe = browser.find_elements_by_tag_name('iframe')[0]#定位iframe框架
        browser.switch_to.frame(iframe)  # 最重要的一步:使用switch_to.frame切换框架

        #print(soup)
        browser.find_element_by_link_text('帐号密码登录').click()

        flag=0#标志位
        old_url = browser.current_url  # 获取旧页面url，用来判断是否跳转来判断是否成功
        print("页面url1",old_url)

        time.sleep(1)
        user_name = browser.find_element_by_id('u')
        password = browser.find_element_by_id('p')
        login_button = browser.find_element_by_id('login_button')

        user_name.clear()
        password.clear()
        user_name.send_keys(cs_acount)
        password.send_keys(cs_passwords)
        login_button.click()

        time.sleep(3)
        new_url = browser.current_url  # 获取当前新页面url
        print("页面url2", new_url)

        if new_url != old_url:  # 判断条件
            flag = 1

        self.assertTrue(flag, "登录失败！原因：账密错误")  # 使用断言来判断测试是否成功，如果失败则以第二个参数为信息写入report




    def test_qqaccount_logon(self):#done(未验证)
        """
        测试点7：注册新QQ账号功能能否实现
        :return:
        """
        browser.find_element_by_link_text('QQ').click()
        time.sleep(2)
        iframe = browser.find_elements_by_tag_name('iframe')[0]  # 定位框架
        browser.switch_to.frame(iframe)  # 最重要的一步，切换框架,不然没法点注册新账号
        #soup = BeautifulSoup(browser.page_source, "html.parser")

        windows = browser.current_window_handle  # 获取当前页面句柄
        browser.find_element_by_link_text('注册新帐号').click()
        time.sleep(2)#等待新页面跳出

        all_handles = browser.window_handles  # 获取全部页面句柄
        for handle in all_handles:  # 遍历全部页面句柄
            if handle != windows:  # 判断条件
                browser.close()  # 切换到新页面前需要把旧的页面关掉
                browser.switch_to.window(handle)  # 切换到新页面

        nickname = browser.find_element_by_id('nickname')
        passwords = browser.find_element_by_id('password')
        tele_number=browser.find_element_by_id('phone')
        send_code=browser.find_element_by_id('send-sms')
        submit = browser.find_element_by_id('get_acc')

        nickname.clear()#清除输入框
        passwords.clear()
        tele_number.clear()

        nickname.send_keys(cs_nickname)#输入昵称
        passwords.send_keys(cs_passwords)#输入密码
        tele_number.send_keys(cs_telenumber)#输入手机号
        send_code.click()#发送验证码

        time.sleep(3)#等待输入验证码
        submit.click()#然后点击登录注册

        flag=self.success_judge(2, 2)  # 循环检测3次，每次3s，等待滑块验证完成
        # 使用断言来判断测试是否成功，如果失败则以第二个参数为信息写入report
        self.assertTrue(flag,"注册失败！原因：many")




    def test_qqfeedback(self):#Done
        """
        测试点8：qq意见反馈页面能否打开
        :return:
        """
        browser.find_element_by_link_text('QQ').click()

        flag = 0
        windows = browser.current_window_handle  # 获取当前页面句柄，用页面是否跳转来判断是否成功

        time.sleep(2)
        iframe = browser.find_elements_by_tag_name('iframe')[0]  # 定位框架
        browser.switch_to.frame(iframe)  # 最重要的一步，切换框架
        soup = BeautifulSoup(browser.page_source, "html.parser")
        #print(soup)
        browser.find_element_by_link_text('意见反馈').click()

        time.sleep(2)  # 等待页面跳出
        #注意：通过句柄的方式只能适用于判断是否有新页面跳出
        all_handles = browser.window_handles  # 获取全部页面句柄
        for handle in all_handles:  # 遍历全部页面句柄
            if handle != windows:  # 判断条件
                browser.close()#切换前关闭旧页面
                browser.switch_to.window(handle)  # 切换到新页面
                flag=1

        self.assertTrue(flag, "意见反馈页面打开失败！原因未知")  # 使用断言来判断测试是否成功，如果失败则以第二个参数为信息写入report
        print("意见反馈页面打开成功！")







# 添加Suite,unittest框架要求
def Suite():
    suiteTest = unittest.TestSuite()##定义一个单元测试容器将测试用例依次加入到容器

    suiteTest.addTest(JD_TestCase("test_account_login"))#1
    suiteTest.addTest(JD_TestCase("test_twodcode_login"))#2
    suiteTest.addTest(JD_TestCase("test_account_logon"))#3
    suiteTest.addTest(JD_TestCase("test_wechat_login"))#4
    suiteTest.addTest(JD_TestCase("test_qqtwodcode_login"))#5
    suiteTest.addTest(JD_TestCase("test_qqaccount_login"))#6
    suiteTest.addTest(JD_TestCase("test_qqaccount_logon"))#7
    suiteTest.addTest(JD_TestCase("test_qqfeedback"))#8

    return suiteTest

if __name__=="__main__":

    #使用unittest配合HTMLTestReport工具，可以自动获取打印在终端中的信息，写入报告
    filePath = report_path  # 确定生成报告的路径
    fp = open(filePath, 'wb')#打开文件

    # 生成报告的Title,描述
    runner = HTMLTestReportCN.HTMLTestRunner(   #实例化类，传入必要参数
        stream=fp,                              #打开好的文件（载入内存）
        title=report_title,                     #题目
        # description='详细测试用例结果',
        tester=testor                                #测试者
    )
    # 运行测试用例
    runner.run(Suite())#Suite里面是所有测试用例
    # 关闭文件，否则会无法生成文件
    fp.close()