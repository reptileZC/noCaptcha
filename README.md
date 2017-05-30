
<img src="https://static.wixstatic.com/media/142a1c_e2711fc04bf84886917e12aa57ff178e~mv2.png/v1/fill/w_49,h_75,al_c,usm_0.66_1.00_0.01/142a1c_e2711fc04bf84886917e12aa57ff178e~mv2.png" width="50" >  

# [NoCaptcha](http://www.nocaptcha.co) ReCaptcha v2 handlers. 


### Core functions handles reCaptcha v2 bot interaction, using ruCaptcha breaking captcha service.

### Library does the following:
 * Selects checkbox 
 * Fetch reCaptcha image/instructions and send to captcha cracking services for a response
 * Ticks response images and submit.
 * Handles errors.

# Instructions
1) Install Selenium 3.0.1
2) Go to core/reCaptcha.py and edit line 61 - reCaptchaKey



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
