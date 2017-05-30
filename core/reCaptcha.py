# -*- coding: utf-8 -*-
"""
Author: Gabriel Munits
Desctiption:
Version:
"""

'''
Instructions:
1) get selenium browser current window" "mainWin = browser.current_window_handle"
2) switch the browser to current window:"browser.switch_to.window(mainWin)"
3) create captcha object "cap = Captcha(self.__browser)"
4) fill captcha checkbox "cap.selectCheckbox()"
5) solve captcha "capIsSolved = cap.Solve()"


All code:

browser = webdriver.Firefox()
browser.get("https://www.google.com/recaptcha/api2/demo")
mainWin = browser.current_window_handle
browser.switch_to.window(mainWin)

captcha = Captcha(browser)
if captcha.Solve():
    print "captcha solved"
else:
    print "captcha failed to solve"



'''
import re
import sys
import logging
# from utils import *  # add utils
import requests
from threading import Thread
import json
import os
import base64
import urllib
import itertools
import random
import subprocess
# Selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchFrameException

import time
from random import uniform
global timetoslve  # time takes to solve
from threading import Thread

__file__ = 'reCaptcha.py'

logger = logging.getLogger(__file__)

# ticking google recaptcha checkbox
rootpath = os.path.dirname(os.path.abspath(__file__))
logsPath = rootpath + '/logs'


global ID
global ruCaptchaKey
global waitForAnswer
global captchaImage


ruCaptchaKey = '419f10cf03eecd326a2c702fe2d50d4a'
waitForAnswer = 30
ID = random.randint(0,1000000)
captchaImageName = 'captcha' + str(ID) + '.jpg'


def wait_between(a, b):
    time.sleep(uniform(a, b))
    pass


class Captcha(object):

    # webdriver instance
    def __init__(self, browser):
        self.__browser = browser
        pass

    def selectCheckbox(self): # checking checkbox
        wait_between(5, 6)
        try:
            # go to captcha
            self.__browser.switch_to_frame(self.__browser.find_elements_by_tag_name("iframe")[0])
            # locate CheckBox web element
            CheckBox = WebDriverWait(self.__browser, 10).until(
                EC.presence_of_element_located((By.ID, "recaptcha-anchor")))
            wait_between(1,2)
            # making click on captcha CheckBox
            CheckBox.click()

            #self.__browser.find_element_by_xpath('//*[@id="recaptcha-anchor"]/div[5]').click()

            # back to main window
            self.__browser.switch_to_default_content()
            # switch to the second iframe by tag name
            logging.info('Captcha checked')
            print ('captcha checked')
            wait_between(10,11)
            return True
        except (NoSuchFrameException, TimeoutException, Exception) as e:
            print (e)
            logger.info(str(e) + 'reCaptcha selectCheckbox() function failed')
            return False
            pass

    def getImage(self): # download captcha image
        wait_between(4, 5)
        try:
            import urllib
            # switch to image iframe
            img = self.__browser.find_element_by_xpath(
                "//*[@id='rc-imageselect-target']/table/tbody/tr[1]/td[2]/div/div[1]/img")
            src = img.get_attribute('src')
            urllib.urlretrieve(src, captchaImageName)  # save image
            logging.info('Got captcha image on url ' + src)
            return True
        except (NoSuchFrameException, NoSuchElementException, IndexError, Exception) as e:
            print (e)
            logger.error(
                'Error retreiving reCaptcha image. Reason {0}'.format(str(e)))
            return False
        pass

    def getInstructions(self): # get image challenge instructions
        wait_between(4,5)
        try:
            try:
                self.__browser.switch_to_frame(self.__browser.find_elements_by_tag_name("iframe")[1])
            except Exception as e:
                pass
            txt = self.__browser.find_element_by_css_selector('.rc-imageselect-desc-no-canonical').text
            return txt
        except (NoSuchElementException, Exception) as e:
            print ('Could not get captcha instructions')
            logger.error('Could not get reCaptcha instructions. Reason {0}'.format(str(e)))
            return ''
        pass

    # get Captchas dimentions -
    #3*3 return 3
    #4*4 return 4
    #4*2 return 2
    def getCaptchaDimention(self):
        d = int(self.__browser.find_element_by_xpath(
            '//div[@id="rc-imageselect-target"]/table').get_attribute("class")[-1])
        return d if d else 3  # dimention is 3 by default

    def kill(self):
        if subprocess.call(["killall", "-9", "firefox-bin"]) > 0:
            print('Firefox cleanup - FAILURE!')
        else:
            print('Firefox cleanup - SUCCESS!')

        sys.exit(1)
        pass

    # refresh captcha image
    def refresh(self):
        # self.__browser.switch_to_frame(
        #    self.__browser.find_elements_by_tag_name("iframe")[0])
        # self.__browser.refresh()
        try:
            self.__browser.find_element_by_xpath(
                '//*[@id="recaptcha-reload-button"]').click()
            wait_between(2, 3)
            print ("refreshed")
        except Exception as e:
            print (e)
            self.kill()


    # solving captcha
    def Solve(self):
        wait_between(1,2)
        instructions = self.getInstructions()  # captcha instructions
        if self.getImage() and instructions is not '' and not None:  # validate image and instructions
            if len(instructions) > 9:# check captcha instructions
                print 'Asking Rucaptcha for answer'
                # ready to receive answer (what images to tick)
                ans = self.request(instructions)
                print ("request Response " + str(ans))
                if ans is not '':
                    if self.tickImages(ans) :
                        # check that what is clicked is valid answer
                        # it can be incorrect answer
                        try:

                            ##### scan for success - otherwise begin all again

                            # check if instructions appear - if not, captcha passed
                            self.__browser.find_element_by_xpath(
                                '//*[@id="recaptcha-verify-button"]').click()
                            wait_between(2, 3)

                            self.__browser.switch_to_default_content()


                            if self.getInstructions():
                                print ("Solving again")
                                self.Solve()
                            else:
                                print ("captcha completed")


                            # click on the submit button in captcha field
                            # self.__browser.switch_to_default_content()
                            '''
                            try:
                                self.__browser.find_element_by_xpath(
                                    '//*[@id="ctl00_plhMain_btnSubmit"]').click()  # click captcha submit
                            except:
                                pass
                            '''


                        except NoSuchElementException as e:
                            # if fails start captcha all over again
                            # logging.error(str(e))
                            self.refresh()
                            self.Solve()
                            return False
                        #
                        # when image are ticked
                        return True
                        pass

                    # captcha ticking images error
                    else:
                        self.refresh()
                        print ("refreshed page error ticking images")
                        self.Solve()
                        pass
                # captcha answer error
                else:
                    self.refresh()
                    self.Solve()

            else:
                print 'Error at captcha img/instructions fetching'
                logging.error('Error at captcha img/instructions fetching')
                return False
                pass

            return False
            pass

        # error with image or instructions
        else:
            self.refresh()
            self.Solve()
            # switch to first iframe
            print ('Error with getting captcha image')
            logging.error('Error with getting captcha image')
            pass

    def checkChBox(self):
        try:
            s = self.__browser.find_element_by_xpath(
                "//*[@aria-checked='true']")
            return True
        except (NoSuchElementException, Exception) as e:
            return False
        pass

    def hasNumbers(self, inputString): # check if string has numbers
        return bool(re.search(r'\d', inputString))

    def request(self, instructions): # sending request to rucaptcha service
        url = 'http://rucaptcha.com/in.php'
        files = {'file': open(captchaImageName, "rb")}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        }
        data = {'key': ruCaptchaKey, 'method': 'post'}
        data = {
            'method': 'post',
            'key': ruCaptchaKey,
            'textinstructions': instructions,
        }

        response = requests.post(url, files=files, data=data) # post with image and instructions
        print ("Response from reCaptcha: " + response.content)
        cID = str(response.content)
        cID = cID[3:] # id for further answer requests
        print cID

        resp_url = 'http://rucaptcha.com/res.php?key=' + \
            ruCaptchaKey + '&action=get&json=1&id=' + cID

        global c
        c = 0


        while c < waitForAnswer:

            try:
                response = requests.get(resp_url, headers=headers)
                print response.content
                data = json.loads(response.content)
                captcha_token = data['request']
                status = data['status']
            except (ValueError, Exception) as e:
                print (e)
                return ''
            if captcha_token == 'CAPCHA_NOT_READY' and status == 0:
                wait_between(3.0, 3.1)
                c = c + 1

            elif captcha_token == 'ERROR_CAPTCHA_UNSOLVABLE' and status == 0:
                print 'captcha failed, trying again.'
                logging.info('Captcha failed, trying again.')
                wait_between(3.0, 3.1)
                c = c + 1
                return ''

            elif captcha_token == 'ERROR_IMAGE_TYPE_NOT_SUPPORTED':
                print 'captcha image type is not supported'
                logging.info('captcha image type is not supported')

                return ''
            elif captcha_token == 'ERROR_WRONG_CAPTCHA_ID':
                print 'Error captcha ID'
                logging.error('Error captcha id')
                return ''

            elif captcha_token == 'ERROR_KEY_DOES_NOT_EXIST':
                print 'Error with rucaptcha key'
                logging.error('Error with rucaptcha key')
                return ''
                pass
            elif captcha_token == 'ERROR_WRONG_ID_FORMAT':
                print 'Error with ID format'
                logging.error('Error with ID format')
                return ''
                pass
            elif captcha_token == 'ERROR_BAD_DUPLICATES':
                print 'Error bad duplicates'
                logging.error('Error bad duplicates')
                return ''
                pass

            elif captcha_token == 'REPORT_NOT_RECORDED':
                print 'Report was not recorded'
                logging.error('Report was not recorded')
                return ''
                pass

            # captcha answer
            elif self.hasNumbers(str(captcha_token.decode('utf-8'))) and status == 1:
                print 'found numbers!'
                logging.info('found captcha {0}'.format(str(captcha_token)))
                return str(captcha_token)
                break
            else:
                return False
                pass
            pass

        pass

    def tickImages(self, stringToTick): # tick captcha images
        global c
        print 'Found Answer! {0}'.format(str(stringToTick))
        l = []

        try:
            for i in stringToTick:
                print i
                if int(i) != 0:
                    l.append(int(i))
        except (ValueError, TypeError, Exception) as e:
            print 'error with captcha answer response'
            return False

        try:
            dim = self.getCaptchaDimention()  # get captcha dimentions
            logging.info('captcha size is {0}'.format(int(dim)))
            print 'Dimention is: ', dim

            wait_between(2, 3)

            if int(dim) == 2:  # 4*2
                for i in l:
                    if i < 3:
                        # append first row
                        self.__browser.find_element_by_xpath(
                            '//div[@id="rc-imageselect-target"]/table/tbody/tr[{0}]/td[{1}]'.format(1, i)).click()
                        pass
                    elif i > 2 and i < 5:
                        # append second row
                        self.__browser.find_element_by_xpath(
                            '//div[@id="rc-imageselect-target"]/table/tbody/tr[{0}]/td[{1}]'.format(2, i - 2)).click()
                        pass
                    elif i > 4 and i < 7:
                        # appden third row
                        self.__browser.find_element_by_xpath(
                            '//div[@id="rc-imageselect-target"]/table/tbody/tr[{0}]/td[{1}]'.format(3, i - 4)).click()
                        pass
                    elif i > 6 and i < 9:
                        # append fourth row
                        self.__browser.find_element_by_xpath(
                            '//div[@id="rc-imageselect-target"]/table/tbody/tr[{0}]/td[{1}]'.format(4, i - 6)).click()
                    else:
                        print 'error clicking a tile'
                        logging.error(
                            'Failed to mark captcha image challange')
                pass

            elif int(dim) == 3:  # 3*3
                for i in l:
                    if i < 4:
                        # append first row
                        self.__browser.find_element_by_xpath(
                            '//div[@id="rc-imageselect-target"]/table/tbody/tr[{0}]/td[{1}]'.format(1, i)).click()
                        pass
                    elif i < 7 and i > 3:
                        # append second row
                        self.__browser.find_element_by_xpath(
                            '//div[@id="rc-imageselect-target"]/table/tbody/tr[{0}]/td[{1}]'.format(2, i - 3)).click()
                        pass
                    elif i > 6 and i < 10:
                        # append third row
                        self.__browser.find_element_by_xpath(
                            '//div[@id="rc-imageselect-target"]/table/tbody/tr[{0}]/td[{1}]'.format(3, i - 6)).click()
                        pass
                    else:
                        print 'error clicking a tile'
                        logging.error(
                            'Failed to mark captcha image challange')

                pass

            elif int(dim) == 4:  # 4*4
                for i in l:
                    if i < 5:
                        # append first row
                        self.__browser.find_element_by_xpath(
                            '//div[@id="rc-imageselect-target"]/table/tbody/tr[{0}]/td[{1}]'.format(1, i)).click()
                        pass
                    elif i > 4 and i < 9:
                        # append second row
                        self.__browser.find_element_by_xpath(
                            '//div[@id="rc-imageselect-target"]/table/tbody/tr[{0}]/td[{1}]'.format(2, i - 4)).click()
                        pass
                    elif i > 8 and i < 13:
                        # append third row
                        self.__browser.find_element_by_xpath(
                            '//div[@id="rc-imageselect-target"]/table/tbody/tr[{0}]/td[{1}]'.format(3, i - 8)).click()
                        pass
                    elif i > 12 and i < 17:
                        # append fourth row
                        self.__browser.find_element_by_xpath(
                            '//div[@id="rc-imageselect-target"]/table/tbody/tr[{0}]/td[{1}]'.format(3, i - 12)).click()
                        pass
                    else:
                        print 'error clicking a tile'
                        logging.error(
                            'Failed to mark captcha image challange')
                pass

            else:
                print 'Error in image dimentions'
                logging.error('Error is image dimentions')
                return False

            logging.info('received captcha answer {0}'.format(
                str(stringToTick)))
            logging.info('time took to solve {0} seconds'.format(c * 3))
            return True
        except Exception as e:
            logging.info(str(e))
            print (e)
            return False
        pass

    def transalate(self,str):
        # make api call to google translate
        pass


class ruAccount(object):

    def __init__(self, key):
        self.__key = key
        pass

    @classmethod
    def getBalance(self, key):
        r = requests.get('http://rucaptcha.com/res.php?key=' +
                         key + '&action=getbalance')
        return str(r.content)

    @staticmethod  # 2013-11-28
    def getStats(self, year=0, data=0, month=0):
        r = requests.get('http://rucaptcha.com/res.php?key=')
        return str(r.content)

    pass
