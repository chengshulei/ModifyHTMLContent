#!C:\Users\chengsl\AppData\Local\Programs\Python\Python36
# -*- coding: utf-8 -*-

import os
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

def operate_input_page(browser):
    links_input_textarea = browser.find_elements_by_tag_name("textarea") # 需要修改的在textarea下面
    for link_input in links_input_textarea:
        temp_textarea_content = link_input.get_attribute("value") # 需要修改的是value
        print(temp_textarea_content) # 修改前的value
        if re.search(r'6.5.0.10412',temp_textarea_content): # 6.5.0.10412版本要特别处理，可能是其中包含特别字符，不能用脚本写入
            print("这里格式有问题，输入后报错，需要手动替换")
        if re.search(r'172.16.0.17',temp_textarea_content): # 判断是否包含需要修改的IP
            temp_textarea_content = temp_textarea_content.replace("172.16.0.17","172.17.18.114") # 获得替换后的value
            print(temp_textarea_content) # 修改后的value
            link_input.clear() # 清空原value
            print("清除当前textarea中的内容")
            link_input.send_keys(temp_textarea_content) # 写入修改后的value
            print("将修改IP后的内容写入textarea中")
            links_submit_button = browser.find_elements_by_tag_name("input")
            for link_submit in links_submit_button:
                submit_button = link_submit.get_attribute("value")
                if "提交变更" in link_submit.get_attribute("value"): # 判断按钮是否是提交变更按钮
                    print("找到提交变更按钮")
                    link_submit.click() # 点击提交变更按钮，之后页面想回跳转
                    browser.back() # 这里让页面重回编辑页面
                    browser.back() # 再次返回让页面回到编辑此页面按钮页面，方便后面再次返回
                    print("提交变更完成")
                    return
                else:
                    print("当前不是提交变更按钮")
                    continue
            print("没有找到提交变更按钮") # 不会执行到这里
            browser.back()
            return
        else:
            print("没有找到要修改的IP")
            browser.back() # IP不需要修改则返回编辑此页面按钮页面
            return

def operate_edit_this_page(browser):
    links_editthispage_page = browser.find_elements_by_tag_name("input")
    for link_editthispage in links_editthispage_page:
        if "编辑此页面" in link_editthispage.get_attribute("value"):
            print("编辑此页面")
            link_editthispage.click() # 点击编辑此页面链接
            operate_input_page(browser); # 进入编辑此页面的页面
            browser.back() # 返回到点击测试链接页面
            return           
                        
def operate_versioncontent_page(browser):
    links_versioncontent_page = browser.find_elements_by_tag_name("a")
    for i in range(len(links_versioncontent_page)):
        link_versioncontent = links_versioncontent_page[i]
        if "点击测试" in link_versioncontent.get_attribute("text"):
            print("点击测试")
            link_versioncontent.click() # 点击点击测试链接
            operate_edit_this_page(browser) # 进入点击测试页面
            links_versioncontent_page = browser.find_elements_by_tag_name("a") # 重新获取a链接元素，否则会报错，因为页面进过了跳转
    operate_edit_this_page(browser) # 页面底部也有编辑此页面，其中也需要修改

def operate_version_page(browser):
    links_version_page = browser.find_elements_by_tag_name("a")
    for i in range(len(links_version_page)):
        link_version = links_version_page[i]
        temp_version = link_version.get_attribute("text")
        if re.search('^v[0-9]{1,2}\.[0-9]{1,2}$',temp_version): # 查找版本号
            print(temp_version) # 打印版本
            link_version.click() # 点击某个版本
            operate_versioncontent_page(browser) # 进入该版本内页面
            links_version_page = browser.find_elements_by_tag_name("a") # 重新获取a链接元素，否则会报错，因为页面进过了跳转
  
if __name__ == "__main__":
    chormedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe" # Chrome驱动
    os.environ["webdriver.chrome.driver"] = chormedriver  #调用chrome浏览器
    #iedriver = "C:\Program Files\Internet Explorer\IEDriverServer.exe" # IE驱动
    #os.environ["webdriver.ie.driver"] = iedriver  #调用IE浏览器
    
    browser = webdriver.Ie(chormedriver)
    browser.get('http://172.17.18.114:8080/2345explorer/login')  #需要打开的网址
    user = browser.find_element_by_id("username") #审查元素username的id
    user.send_keys("wanggh")  #输入账号
    password = browser.find_element_by_name("password") #审查元素password的name
    password.send_keys("wanggh")  #输入密码
    password.send_keys(Keys.RETURN) #实现自动点击登陆
    print("登陆成功")

    links_homepage = browser.find_elements_by_tag_name("a") # 获取a链接元素
    for link_home in links_homepage:
        if "历史版本" in link_home.get_attribute("text"): # 查找历史版本链接
            print("历史版本")
            link_home.click() # 点击历史版本，跳转
            break
    operate_version_page(browser) # 从历史版本页面开始进行
    sleep(2)
    browser.close() #关闭浏览器
    


