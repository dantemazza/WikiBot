from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import time

# gmail: *********@gmail.com
# twitter user: WikiBot2
# password: *************

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

def generateWikiTweet(text, hashtag):
    wikiChars = list(text)
    characters = []
    isInTag = False
    index = 0
    length = 0
    hashLength = len(hashtag)
    while index < len(wikiChars) and length < 250-hashLength:
        if length > 140:
            if characters[length - 1] == '.':
                break
        if isInTag:
            if wikiChars[index] == '>' or wikiChars[index] == ']':
                isInTag = False
        else:
            if wikiChars[index] == '&':
                index +=6
                continue
            if wikiChars[index] == '<' or wikiChars[index] == '[':
                isInTag = True
            else:
                characters.append(wikiChars[index])
                length += 1
        index += 1
    if length > 2:
        characters.append(hashtag)
    return ''.join(characters)

def generateHashtag(title):
    chars = list(title)
    hashChars = [' #']
    length = len(chars)
    isInBrackets = False

    for i in range(0, length):
        if isInBrackets:
            if chars[i] == ')':
                isInBrackets = False
        else:
            if chars[i] == '(':
                isInBrackets = True
            else:
                if chars[i] == ',':
                    hashChars.append(" #")
                elif chars[i] != ' ' and chars[i] != '.' and chars[i] != "'" and chars[i] != '-':
                    hashChars.append(chars[i])
    return ''.join(hashChars)

def deployWikiTweet():
    browser.switch_to.window(wikipedia)
    body = browser.find_element_by_xpath("//body")
    body.send_keys(Keys.ALT, Keys.SHIFT, 'x')

    text = browser.find_element_by_xpath("//p").get_attribute('innerHTML')

    title = browser.find_element_by_xpath("//h1").get_attribute('innerHTML')
    titleMinusHTML = generateWikiTweet(title, "")
    hashtag = generateHashtag(titleMinusHTML)
    tweet = generateWikiTweet(text, hashtag)

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
        try:
            deployWikiTweet()
            time.sleep(0.25)
        except NoSuchElementException:
            browser.switch_to.window(twitter)
            print("NoSuchElementException")
    except WebDriverException:
        print("WebDriverException")




