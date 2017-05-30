# noCaptcha
ReCaptcha bridge for multi-language support 



Instructions: 

# Running core
```python

browser = webdriver.Firefox() # creating browser
browser.get("https://www.google.com/recaptcha/api2/demo") # open target page
mainWin = browser.current_window_handle 
browser.switch_to.window(mainWin) # switch to main frame

captcha = Captcha(browser) # create Captcha object
if captcha.Solve():
    print "captcha solved"
else:
    print "captcha failed to solve"

```
