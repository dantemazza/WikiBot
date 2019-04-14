from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time

# gmail: *********@gmail.com
# twitter user: WikiBot2
# password: *************

username = "WikiBot2"
password = "*************"
browser = webdriver.Chrome('C:\\Users\\dante\\Downloads\\chromedriver_win32\\chromedriver')
browser.get('https://twitter.com/login')

userBar = browser.find_element_by_xpath("//div[@class='clearfix field']//input[@name='session[username_or_email]']")
passBar = browser.find_element_by_xpath("//div[@class='clearfix field']//input[@name='session[password]']")

userBar.click()
userBar.send_keys(username)
passBar.click()
passBar.send_keys(password)

logInButton = browser.find_element_by_xpath("//div[@class='clearfix']//button[@type='submit']")
logInButton.click()

twitter = browser.window_handles[0]

browser.execute_script("window.open('https://en.wikipedia.org/wiki/Main_Page', 'wikipedia')")

wikipedia = browser.window_handles[1]


browser.switch_to.window(twitter)

def generateWikiTweet(text):
    wikiChars = list(text)
    characters = []
    isInTag = False
    index = 0
    length = 0
    while not(length > 140 and characters[length - 1] == '.') and index < len(wikiChars) and (length < 250):
        if isInTag:
            if wikiChars[index] == '>' or wikiChars[index] == ']' or wikiChars[index] == '&':
                isInTag = False
        else:
            if wikiChars[index] == '<' or wikiChars[index] == '[' or wikiChars[index] == ';':
                isInTag = True
            else:
                characters.append(wikiChars[index])
                length += 1
        index += 1
    return ''.join(characters)

def deployWikiTweet():
    browser.switch_to.window(wikipedia)
    body = browser.find_element_by_xpath("//body")
    body.send_keys(Keys.ALT, Keys.SHIFT, 'x')

    text = browser.find_element_by_xpath("//p").get_attribute('innerHTML')

    tweet = generateWikiTweet(text)

    browser.switch_to.window(twitter)
    tweetBox = browser.find_element_by_xpath("//div[@class='tweet-box rich-editor']//div")
    tweetBox.click()

    time.sleep(0.25)

    actions = ActionChains(browser)
    actions.send_keys(tweet)
    actions.perform()

    tweetButton = browser.find_element_by_xpath("//span[@class='button-text tweeting-text']")
    tweetButton.click()

for i in range(1,303):
    try:
        deployWikiTweet()
        time.sleep(0.25)
    except NoSuchElementException:
        browser.switch_to.window(twitter)



