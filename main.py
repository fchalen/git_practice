from resources import Newspaper
import datetime as dt
import pandas as pd

newspaper_urls = ['https://www.infobae.com/?noredirect', 'https://www.pagina12.com.ar/', 'https://www.minutouno.com/',
                 'https://www.tn.com.ar/', 'https://www.ellitoral.com/', 'https://www.clarin.com']
for url in newspaper_urls:
    newspaper = Newspaper(url)
    newspaper.get_article_titles()
    now = dt.datetime.now().strftime("%Y_%m_%d_%H_%M")
    data = {'Datetime': dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Newspaper': newspaper.name,
            'Headline': newspaper.news_titles, 'URL': newspaper.news_urls_list
            }
    df = pd.DataFrame(data, columns=['Datetime', 'Newspaper', 'Headline', 'URL'])
    df.to_csv(f'{now}_{newspaper.name}_headlines.csv')
    


