# noCaptcha
ReCaptcha bridge for multi-language support 



Instructions: 

#How to run core

browser = webdriver.Firefox()
browser.get("https://www.google.com/recaptcha/api2/demo")
mainWin = browser.current_window_handle
browser.switch_to.window(mainWin)

captcha = Captcha(browser)
if captcha.Solve():
    print "captcha solved"
else:
    print "captcha failed to solve"

