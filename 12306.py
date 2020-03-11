"""自动抢票"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class Qiangpiao(object):
    def __init__(self):
        # 登陆url
        self.login_url = 'https://kyfw.12306.cn/otn/resources/login.html'
        # 登陆成功后跳转的url
        self.in_url = 'https://kyfw.12306.cn/otn/view/index.html'
        # 查票
        self.search = 'https://www.12306.cn/index/index.html'
        # 订票
        self.passenger_url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        self.driver = webdriver.Firefox()
    def wait_input(self):
        self.from_station = input('出发地：')
        self.to_station = input('目的地:')
        self.depart_time = input('出发时间:')
        self.passengers = input('乘客姓名：').split(',')
        self.trains = input('车次：').split(',')

    def _login(self):
        self.driver.get(self.login_url)
        # 显示等待:每隔一段时间检测一次当前页面元素是否存在，如果超过设置时间检测不到则抛出异常
        WebDriverWait(self.driver,1000).until(
            EC.url_to_be(self.in_url)
        )
        print('登陆成功')
        # 隐式等待:不管条件副不符合都等待指定时间
    def _order_ticket(self):
        # 跳转到查票
        self.driver.get(self.search)
        # 等待出发地是否输入正确
        WebDriverWait(self.driver,1000).until(
            EC.text_to_be_present_in_element_value((By.ID,'fromStationText'),self.from_station)
        )
        # 等待出发地是否输入正确
        WebDriverWait(self.driver,1000).until(
            EC.text_to_be_present_in_element_value((By.ID,'toStationText'),self.to_station)
        )
        # 等待时间是否输入正确
        WebDriverWait(self.driver,1000).until(
            EC.text_to_be_present_in_element_value((By.ID,'train_date'),self.depart_time)
        )
        # 等待点击查询按钮
        WebDriverWait(self.driver,1000).until(
            EC.element_to_be_clickable((By.ID,'search_one'))
        )
        # 如果能够被点击,找到按钮执行点击事件
        self.driver.find_element_by_id('search_one').click()

        # 在点击查询按钮之后，等待车次信息是否刷新出来
        WebDriverWait(self.driver,100).until(
            EC.presence_of_element_located((By.XPATH,"//tbody[@id='queryLeftTable']/tr"))
        )
        # time.sleep(3)
        # 找到所有没有datatran属性的就是车次标签
        tr_list = self.driver.find_elements_by_xpath("//tbody[@id='queryLeftTable']/tr[not(@datatran)]")
        # print(tr_list)

        #遍历所有的满足条件的tr标签
        for tr in tr_list:
            train_number = tr.find_element_by_class_name('number').text
            # print(train_number)
            # print('='*20)
            if train_number in self.trains:
                left_ticket_td = tr.find_element_by_xpath('.//td[4]').text
                if left_ticket_td == '有' or left_ticket_td.isdigit:
                    print(train_number+'有票')
                    orderbtn = tr.find_element_by_class_name('btn72')
                    orderbtn.click()
                    # 等待是否来到乘客页面
                    WebDriverWait(self.driver,1000).until(
                        EC.url_to_be(self.passenger_url)
                    )
                    # 等待乘客信息是否加载进来
                    WebDriverWait(self.driver,1000).until(
                        EC.presence_of_element_located((By.XPATH,".//ul[@id='normal_passenger_id']/li"))
                    )
                    # 获取乘客所有信息
                    passnger_labels = self.driver.find_elements_by_xpath(".//ul[@id='normal_passenger_id']/li/label")
                    for passnger_label in passnger_labels:
                        name = passnger_label.text
                        if name in self.passengers:
                            passnger_label.click()
                    # 获取提交订单的按钮
                    submitbtn = self.driver.find_element_by_id('submitOrder_id')
                    submitbtn.click()
                    # 判断订单是否加载出来
                    WebDriverWait(self.driver,1000).until(
                        EC.presence_of_element_located((By.CLASS_NAME,'dhtmlx_wins_body_outer'))
                    )
                    # 如果却人按钮出现点击
                    WebDriverWait(self.driver,1000).until(
                        EC.presence_of_element_located((By.ID,'qr_submit_id'))
                    )
                    confirmbtn = self.driver.find_element_by_id('qr_submit_id')
                    confirmbtn.click()
                    while confirmbtn:
                        confirmbtn.click()
                        confirmbtn = self.driver.find_element_by_id('qr_submit_id')
                    return 
    def run(self):
        self.wait_input()
        self._login()
        self._order_ticket()

if __name__ == '__main__':
    Qiangpiao().run()







