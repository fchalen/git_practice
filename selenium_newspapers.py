import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

url_1='https://www.clarin.com'

def driver(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("window-size=1400,1500")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("start-maximized")
    options.add_argument("enable-automation")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    wdriver = webdriver.Chrome(options=options, executable_path='C:/Users/franc/Documents/PyCharm Projects/NewsScrapper/chromedriver.exe')
    #wdriver = webdriver.Firefox('C:/Users/franc/Documents/PyCharm Projects/NewsScrapper/chromedriver.exe')

    wdriver.get(url)

    #INFINITE SCROLL START
    scroll_pause_time = 0.8

    # Get scroll height
    last_height = wdriver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        wdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = wdriver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    #INFINITE SCROLL END
    return wdriver



def set_clarin_titles_urls(driver):
    # Get articles by CSS selector
    arts = driver.find_elements_by_css_selector('article')
    urls = []
    titles = []
    #For each article get
    for article in arts:
        try:
            head = article.find_element_by_css_selector('h1, h2, h3')
            url = article.find_element_by_css_selector('a')
            titles.append(head.get_attribute('textContent'))
            urls.append(url.get_attribute('href'))
        except:
            continue
    return titles, urls

    driver.close()

def set_lanacion_titles_urls(driver):
    # Get articles by CSS selector
    arts = driver.find_elements_by_css_selector('article')
    urls = []
    titles = []
    #For each article get
    for article in arts:
        try:
            head = article.find_element_by_css_selector('h1, h2, h3')
            url = article.find_element_by_css_selector('a')
            titles.append(url.get_attribute('title'))
            urls.append(url.get_attribute('href'))
        except:
            continue
    return titles, urls
    driver.close()

#driver_1 = driver(url_1)
#titles, urls = set_lanacion_titles_urls(driver_1)
#df = pd.DataFrame({'urls': urls, 'titles': titles})
#print(df.head(10))
#print(df.head())
#print(df.shape)
#print(len(df))