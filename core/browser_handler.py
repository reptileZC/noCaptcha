import os
import sys
import reCaptcha
import subprocess
from reCaptcha import *
try:
    from selenium import webdriver
    from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    from selenium.webdriver.support.ui import WebDriverWait
    # no element matching exception
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import NoSuchElementException
    from selenium.common.exceptions import TimeoutException
    from selenium.common.exceptions import NoSuchFrameException
    from selenium.webdriver.common.by import By
except ImportError as e:
    print ("Import Error: {0}".format(e))


def killAll():
    if subprocess.call(["killall", "-9", "firefox-bin"]) > 0:
        print('Firefox cleanup - FAILURE!')
    else:
        print('Firefox cleanup - SUCCESS!')
    pass

def brows_conf():
    try:
        os.environ[
            "PATH"] += ":/usr/local/lib/python2.7/site-packages/selenium-3.0.1-py2.7.egg/selenium/webdriver/firefox"
        binary = '/Applications/TorBrowser.app/Contents/MacOS/firefox'
        firefox_capabilities = DesiredCapabilities.FIREFOX
        # on selenium 3 version Marionette is enabled by default
        firefox_capabilities['marionette'] = True
        firefox_capabilities['binary'] = binary
        # disablinf all browser add-ons, popups
        profile = webdriver.FirefoxProfile()
        profile.set_preference("pdfjs.disabled", True)
        profile.set_preference("dom.disable_beforeunload", True)
        profile.set_preference('dom.successive_dialog_time_limit', 0)
        profile.set_preference("http.response.timeout", 10)
        # dom.successive_dialog_time_limit 0
        browser = webdriver.Firefox(
            capabilities=firefox_capabilities, firefox_profile=profile)
        print ('created browser')
    except Exception as e:
        print (e)
    #browser.get("https://www.google.com/recaptcha/api2/demo")
    #browser.get("http://www.zbuyer.com/reCaptchaCheck.aspx?c=http%3a%2f%2fwww.zbuyer.com%2fAvailableProperties2.aspx")
    #browser.get("https://www.jeuxvideo.com/login")
    browser.get("https://docs.google.com/forms/d/e/1FAIpQLSeq7FaJY89ZUpzRIUus1SLM84izKYm0C7n70l8_pf2vA5iiGA/viewform?c=0&w=1")
    mainWindow = browser.current_window_handle
    browser.switch_to.window(mainWindow)
    
    pass
    

if __name__ == '__main__':
    

    captcha = Captcha(browser)
    captcha.selectCheckbox()

    if captcha.Solve():
        print "captcha solved"
    else:
        print "captcha failed to solve"


    killAll()
