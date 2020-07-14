import time
from selenium import webdriver
import pandas as pd

url_1='https://www.clarin.com'

def driver(url):
    wdriver = webdriver.Firefox()

    wdriver.get(url)

    #INFINITE SCROLL START
    scroll_pause_time = 0.5

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

#set_clarin_urls(wdriver)
driver_1 = driver(url_1)
titles, urls = set_clarin_titles_urls(driver_1)
df = pd.DataFrame({'urls': urls, 'titles' : titles})
print(df.head(10))
df.to_csv('clarin.csv')
#print(df.head())
#print(df.shape)