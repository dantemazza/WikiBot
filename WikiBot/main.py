from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import time

# gmail: ********@gmail.com
# twitter user: WikiBot2
# password: ***********
start = time.time()
username = "WikiBot2"
password = "***********"
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
startTweets = browser.find_element_by_xpath("//span[@class='ProfileCardStats-statValue']").get_attribute('innerHTML')
startTweets = startTweets.replace(',', '')
print(f"Current tweet count: {startTweets}")
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
    if length >= 250-hashLength:
        characters.append("...")
    if length > 25 or hashtag == '':
        characters.append(hashtag)
    else:
        return ''
    return ''.join(characters)

def generateHashtag(title):
    chars = list(title)
    hashChars = [' #']
    length = len(chars)
    isInBrackets = False
    breakIntoMultiple = True if len(chars) > 21 else False
    for i in range(0, length):
        if isInBrackets:
            if chars[i] == ')':
                isInBrackets = False
        else:
            if chars[i] == '(':
                isInBrackets = True
            else:
                if (chars[i] == ',' or chars[i] == '–') and not(breakIntoMultiple):
                    breakIntoMultiple = True
                elif ((chars[i] == ' ' and chars[i+1] != '(') or chars[i] == '-') and breakIntoMultiple:
                    hashChars.append(" #")
                elif chars[i] != ' ' and chars[i] != '.' and chars[i] != "'" and chars[i] != ',' and chars[i] != ':':
                    hashChars.append(chars[i])
    return ''.join(hashChars)

def deployWikiTweet():
    browser.switch_to.window(wikipedia)
    body = browser.find_element_by_xpath("//body")
    body.send_keys(Keys.ALT, Keys.SHIFT, 'x')

    title = browser.find_element_by_xpath("//h1").get_attribute('innerHTML')
    if title[0:4] == 'List':
        browser.switch_to.window(twitter)
        return

    text = browser.find_element_by_xpath("//p").get_attribute('innerHTML')

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

#twitter appears to have a semi-hourly limit of 300 tweets - the settings below are configured accordingly for a day
for k in range(9):
    for i in range(301):
        try:
            try:
                deployWikiTweet()
                time.sleep(0.25)
            except NoSuchElementException:
                browser.switch_to.window(twitter)
                print("NoSuchElementException")
        except WebDriverException:
            print("WebDriverException")
    time.sleep(1800)

end = time.time()
browser.refresh()

endTweets = browser.find_element_by_xpath("//span[@class='ProfileCardStats-statValue']").get_attribute('innerHTML')
endTweets = endTweets.replace(',', '')

totalTweets = int(endTweets) - int(startTweets)
avg = totalTweets / (end-start) * 60

print(f"{totalTweets} tweets were generated at an average rate of " + str(avg)[0:4] + " tweets per minute.")
browser.quit()

