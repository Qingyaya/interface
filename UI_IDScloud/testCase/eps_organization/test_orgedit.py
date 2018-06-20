#-*-coding:utf-8 -*-
import time
from ddt import ddt,data
from selenium import webdriver
from page_objects.eps_organization import Epsorg
from public.get_csv import *
from datas.setting import *
from public.Log import Log
import unittest
import pymysql
from random import choice

log=Log()
ScreenPath = log.get_screenshot_path(__name__)

datas=get_data(BASE_DIR+'\\datas\\edit_org.csv')

@ddt
class Epsorganization_edit(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        log.info('===================test_editorg==============================')
        Screen = os.path.join(ScreenPath, 'test_EpsorganizationLogin_error.png')
        cls.Mdriver=webdriver.Chrome()
        cls.Mdriver.maximize_window()
        cls.Mdriver.get(EPS_URL)
        cls.epsorg=Epsorg(cls.Mdriver)
        cls.epsorg.Login(EPS_name,EPS_pwd,Screen)

    def setUp(self):
        Screen = os.path.join(ScreenPath, 'test_setup_error.png')
        self.Mdriver.refresh()
        self.epsorg.intopage(Screen)


    @data(*datas)
    def test_editorg(self,data):
        Screen = os.path.join(ScreenPath, 'test_editorg_%s_error.png' % data['caseNo'])
        self.epsorg.choose_org(data['oldorgname'],Screen)
        if data['buttonstate'] == 'None':
            self.epsorg.editbutton_click(Screen)
            self.epsorg.editorgpage(data['orgNo'], data['orgname'], data['comment'], Screen)
            self.epsorg.editorgok(Screen)
            if data['error'] !='':
                errormsg=data['error'].split('/')
                try:
                    msgs=self.epsorg.addpage_error(Screen)
                    self.epsorg.addorgcancle(Screen)
                    retA=[i for i in errormsg if i not in msgs]
                    retB=[i for i in msgs if i not in errormsg]
                    if len(retA) ==0 and len(retB)==0:
                        flag=True
                        msg='页面报错信息正确：%s' % errormsg
                        self.Mdriver.save_screenshot(os.path.join(ScreenPath,'test_addorg_%s_pass.png' % data['caseNo']))
                    else:
                        flag=False
                        msg='报错信息应该是：%s,页面的报错信息是：%s' %(errormsg,msgs)
                        self.Mdriver.save_screenshot(os.path.join(ScreenPath,'test_addorg_%s_fail.png' % data['caseNo']))

                except Exception as e:
                    flag = False
                    msg = e
            else:
                try:
                    self.epsorg.choose_org(data['oldorgname'], Screen)
                    flag = True
                    msg = "修改机构 %s 成功" % (data['oldorgname'])
                    self.Mdriver.save_screenshot(os.path.join(ScreenPath, 'test_editorg_%s_pass.png' % data['caseNo']))

                except:
                    flag = False
                    msg = "修改机构 %s 失败" % (data['oldorgname'])
                    self.Mdriver.save_screenshot(os.path.join(ScreenPath, 'test_editorg_%s_fail.png' % data['caseNo']))
            log.info(msg)
            self.assertTrue(flag, msg)
        else:
            if data['buttonstate']== self.epsorg.editbutton_state(Screen):
                msg='机构不可编辑'
                flag = True
            else:
                msg='机构应不可编辑，目前状态为%s'% self.epsorg.editbutton_state(Screen)
                flag =False
            log.info(msg)
            self.assertTrue(flag,msg)


    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        Screen = os.path.join(ScreenPath, 'test_EpsorganizationLogout_error.png')
        cls.epsorg.Logout(Screen)
        cls.Mdriver.quit()
        log.info('==========================END=================================')


if __name__ == '__main__':
    unittest.main()