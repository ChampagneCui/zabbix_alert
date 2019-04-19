#!/opt/env3.6.8/bin/python
from selenium import webdriver
import time, sys,os
import oss2

from dingtalkchatbot.chatbot import DingtalkChatbot

# WebHook地址
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxxxxxxxxxxxxx'
# 初始化机器人小丁
xiaoding = DingtalkChatbot(webhook)

AccessKeyID = 'xxxxxxxxxxxxxxxxxxxxx' #给oss用的
AccessKeySecret = 'xxxxxxxxxxxxxxxxxxxx'
bucket_name = 'ops-pic'   #oss的bucket名字


def parse_error_msg(text):
        msg = eval(text)
        itemid = msg['监控项ID']
        pic_url = capture_zabbix(itemid)
        dingding(msg, pic_url)

def capture_zabbix(itemid):
        url = 'http://your_zabbix_url/history.php?action=showgraph&itemids[]=' + str(itemid)
        browser = webdriver.PhantomJS("/opt/phantomjs-2.1.1-linux-x86_64/bin/phantomjs",service_log_path=os.path.devnull)
        index = "http://your_zabbix_url/index.php"
        browser.set_window_size(1920, 1080)
        browser.get(index)

        time.sleep(1)
        username = browser.find_element_by_name("name")
        password = browser.find_element_by_name("password")
        username.send_keys("zabbix_username")
        password.send_keys("zabbix_password")
        browser.find_element_by_xpath("//*[@type='submit']").click()
        browser.get(url)
        time.sleep(3)

        pic_path = r'/tmp/' + 'ops_' + str(itemid) + '_' + str(int(time.time())) + '.png'
        browser.save_screenshot(pic_path)
        browser.close()
        pic_url = save_oss(pic_path)
        return pic_url



def save_oss(pic_path):
        auth = oss2.Auth(AccessKeyID, AccessKeySecret)

        bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', bucket_name)
        pic_name = pic_path.split('/')[-1]
        bucket.put_object_from_file(pic_name, pic_path)
        oss_url = 'https://ops-pic.oss-cn-hangzhou.aliyuncs.com/'
        pic_url = oss_url + pic_name
        return pic_url


def text_msg(msg):
        text_msgs = '#### 运维告警'+'\n'
        for i in msg:
                text_msgs += (str(i) + ':' + str(msg[i]) + ',\n'+'\n')
        return text_msgs


def dingding(error_msg, pic_url):
        error_msg = text_msg(error_msg)
        error_msg += ("> ![告警](%s)" %(pic_url)+'\n')
        # Text消息@所有人
        xiaoding.send_markdown(title='告警', text=str(error_msg)
                               )


if __name__ == '__main__':
        text = sys.argv[1]
        parse_error_msg(text)