# NoCaptcha Description
### Core functions handles reCaptcha v2 bot interaction. 
### Library does the following:

###### *) Selects checkbox 
###### *) Fetch reCaptcha image/instructions and send to captcha cracking services for a response
###### *) Ticks response images and submit.
###### *) Handles errors.



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
