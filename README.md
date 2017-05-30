
<img src="https://wix.logotypemaker.com/lKmzXmN6K_WgLMOlM69XWAzB_pg1B69M_1vKbQNlLrmO0AvzrXBQ90bp6rvp.png?v=3" width="180" style="inline-block"> 

# [NoCaptcha](http://www.nocaptcha.co)  ReCaptcha v2 handlers.


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
