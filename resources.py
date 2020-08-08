import requests
from bs4 import BeautifulSoup
import datetime as dt
from collections import Counter
import pandas as pd
from selenium_newspapers import *


today = dt.date.today().strftime("%Y/%m")
blacklist_infobae = ['https', 'http', 'www.infobae.com']
blacklist_p12 = ['/suplementos/', '/opinion']


class Newspaper:

    def __init__(self, url):
        self.url = url
        self.name = url[url.find('www.') + 4:url.find('.com')]
        self.r = requests.get(url)
        self.soup = BeautifulSoup(self.r.text, 'html.parser')
        self.news_urls_list = []
        self.news_titles = []
        self.all_articles = []
        self.most_common_words = []

    def __str__(self):
        """
        String version of the class Newspaper, returns name and date

        """
        return f'Diario {self.name} del dia {dt.date.today().strftime("%Y/%m")}'

    def help(self):
        pass

    def get_article_urls(self):
        """
        Getter of article URLs with specific methods for each newspaper, checks if url list already populated before
        running the method
        """
        # INFOBAE
        if self.name == 'infobae':
            if not self.news_urls_list:
                self.set_infobae_urls_opt()
                return self.news_urls_list
            else:
                return self.news_urls_list
        # PAGINA 12
        elif self.name == 'pagina12':
            if not self.news_urls_list:
                self.set_p12_urls()
                return self.news_urls_list
            else:
                return self.news_urls_list
        # MINUTO 1
        elif self.name == 'minutouno':
            if not self.news_urls_list:
                self.set_minutouno_urls()
                return self.news_urls_list
            else:
                return self.news_urls_list
        # TN
        elif self.name == 'tn':
            if not self.news_urls_list:
                self.set_tn_urls()
                return self.news_urls_list
            else:
                return self.news_urls_list
        # EL LITORAL
        elif self.name == 'ellitoral':
            if not self.news_urls_list:
                self.set_litoral_urls()
                return self.news_urls_list
            else:
                return self.news_urls_list
        # CLARIN
        elif self.name == 'clarin':
            self.set_clarin_urls()
            return self.news_urls_list
        else:
            return self.news_urls_list
        # LA NACION
        #elif self.name == 'lanacion':
        #    self.set_clarin_urls()
        #    return self.news_urls_list
        #else:
        #    return self.news_urls_list

    def get_article_titles(self):
        """
        Getter of article titles with specific methods for each newspaper, checks if url list already populated before
        running the method
        """
        # INFOBAE
        if self.name == 'infobae':
            self.set_infobae_titles_opt()
            return self.news_titles
        # PAGINA 12
        elif self.name == 'pagina12':
            self.set_p12_titles_opt()
            return self.news_titles
        # MINUTO 1
        elif self.name == 'minutouno':
            self.set_minutouno_titles()
            return self.news_titles
        # TN
        elif self.name == 'tn':
            self.set_tn_titles()
            return self.news_titles
        # EL LITORAL
        elif self.name == 'ellitoral':
            self.set_litoral_titles()
            return self.news_titles
        # CLARIN
        elif self.name == 'clarin':
            self.set_clarin_titles()
            return self.news_titles
        # LA NACION
        elif self.name == 'lanacion':
            self.set_lanacion_titles()
            return self.news_titles

    def get_info(self):
        """
        Prints general information about the newspaper
        """
        print('Diario: ', self.name.capitalize())
        print('Edicion del dia:', dt.date.today().strftime('%d/%m/%Y'))
        print('URL:', self.url)
        twitter_address = self.soup.find('meta', {'name': 'twitter:creator'}).attrs['content']
        print('Cuenta de Twittwer:', twitter_address)

    def get_all_articles(self):
        """
        For each article URL creates an instance of the class Article to extract use its defined methods
        """
        for urls in self.news_urls_list:
            article = Article(urls)
            headline = article.get_headline()
            body = article.get_body()
            full_article = str(headline) + str(body)
            self.all_articles.append(full_article)
        return self.all_articles

    def set_infobae_urls_opt(self):
        """
        Sets the variable news_urls_list to a list with all the article URLs in the INFOBAE newspaper
        Returns the list with all urls
        Checks against blacklist to ignore URLs that do not link to articles
        """
        if not self.news_urls_list:
            body = self.soup.find('body')
            headline_elems = body.find_all('div', {'class': 'headline normal normal-style'})
            headline_elems.extend(body.find_all('div', {'class': 'headline small normal-style'}))
            headline_elems.extend(body.find_all('div', {'class': 'headline x-large normal-style'}))
            headline_elems.extend(body.find_all('div', {'class': 'headline huge normal-style'}))
            headline_elems.extend(body.find_all('div', {'class': 'headline xx-large normal-style'}))
            headline_elems.extend(body.find_all('div', {'class': 'headline x-small normal-style'}))
            for element in headline_elems:
                if any([x in element.find('a').attrs['href'] for x in blacklist_infobae]):
                    news_url = element.find('a').attrs['href']
                    self.news_urls_list.append(news_url)
                else:
                    news_url = 'https://www.infobae.com' + element.find('a').attrs['href']
                    self.news_urls_list.append(news_url)

    def set_infobae_urls(self):
        """
        ----- DEPRECATED -----
        Sets the variable news_urls_list to a list with all the article URLs in the INFOBAE newspaper
        Returns the list with all urls
        Checks against blacklist to ignore URLs that do not link to articles
        """
        print('Deprecated method, use set_infobae_urls_op() instead')
        if not self.news_urls_list:
            body = self.soup.find('body')
            # Elimino la barra navegadora de arriba y el menu lateral
            body.find('div', {'id': 'siteheader'}).decompose()
            # Elimino el footer
            body.find('div', {
                'class': 'wrapper clearfix full pb-feature pb-layout-item pb-f-global-footer-colored'}).decompose()
            # Elimino spacers con urls
            body.find('div', {'class': 'toggle-container'}).decompose()
            body.find('div', {'class': 'hot-topics-wrapper'}).decompose()
            for tag in body.select('div[class*="pb-font-smoothing label label-bar label-with-background"]'):
                tag.decompose()
            for tag in body.select('div[class*="label-wrapper text-align-center"]'):
                tag.decompose()
            for tag in body.select('div[class*="label-wrapper text-align-inherit"]'):
                tag.decompose()
            for tag in body.select('h3[class="header-label"]'):
                tag.decompose()
            headlines = body.find_all('a')
            for news in headlines:
                if 'href' in news.attrs:
                    if any([x in news.get('href') for x in blacklist_infobae]):
                        news_url = news.get('href')
                        self.news_urls_list.append(news_url)
                    else:
                        news_url = 'https://www.infobae.com' + news.get('href')
                        self.news_urls_list.append(news_url)
            # Elimino URLs duplicadas
            self.news_urls_list = list(set(self.news_urls_list))
        else:
            pass

    def set_p12_urls(self):
        """
        Sets the variable news_urls_list to a list with all the article URLs in the PAGINA 12 newspaper
        Returns the list with all urls
        Checks against blacklist to ignore URLs that do not link to articles
        """
        if not self.news_urls_list:
            div = self.soup.find_all('div', {'class': 'article-title'})
            for item in div:
                if 'https://www.pagina12.com.ar' in item.find('a').attrs['href']:
                    # Chequeo que no sean URLs en blacklist
                    if any(x in item.find('a').attrs['href'] for x in blacklist_p12):
                        pass
                    else:
                        news_url = item.find('a').attrs['href']
                        self.news_urls_list.append(news_url)
        else:
            pass

    def set_tn_urls(self):
        """
        Sets the variable news_urls_list to a list with all the article URLs in the TN newspaper
        Returns the list with all urls
        Checks against blacklist to ignore URLs that do not link to articles
        """
        if not self.news_urls_list:
            body = self.soup.find('body', {'class': 'page--cover-tn'})
            list_page_cover = body.find_all('h2', {'class': 'article-brick__title'})
            for element in list_page_cover:
                url_part = element.find('a').attrs['href']
                complete_tn_url = 'http://www.tn.com.ar' + url_part
                self.news_urls_list.append(complete_tn_url)
        else:
            pass

    def set_minutouno_urls(self):
        """
        Sets the variable news_urls_list to a list with all the article URLs in the Minuto Uno newspaper
        Returns the list with all urls
        Checks against blacklist to ignore URLs that do not link to articles
        """
        # Chequeo si la lista no tiene nada
        if not self.news_urls_list:
            # si no tiene, seteo el body
            body = self.soup.find("body")
            # elimino todos los scripts adentro del body
            for sc in body("script"):
                sc.decompose()
            # seteo los headlines para levantar los titulos y URLS
            headlines = body.find_all("h2", {"class": "title"})
            for x in headlines:
                y = x.find('a', href=True)
                if x.find('a') == None:
                    pass
                else:
                    try:
                        news_url = x.find("a").attrs['href']
                        self.news_urls_list.append(news_url)
                    except:
                        pass
        else:
            pass

    def set_litoral_urls(self):
        """
        Sets the variable news_urls_list to a list with all the article URLs in the EL LITORAL newspaper
        Returns the list with all urls
        Checks against blacklist to ignore URLs that do not link to articles
        """
        if not self.news_urls_list:
            h1 = self.soup.find_all('h1', {'class' : 'um_titulo entry-title'})
            for header in h1:
                news_url = self.url + header.find('a').attrs['href']
                self.news_urls_list.append(news_url)

        else:
            pass

    def set_clarin_urls(self):
        """
        Sets the variable news_urls_list to a list with all the article URLs in the CLARIN newspaper
        Returns the list with all urls
        Checks against blacklist to ignore URLs that do not link to articles
        """
        if not self.news_urls_list:
            webdriver = driver(self.url)
            clarin_titles, clarin_urls = set_clarin_titles_urls(webdriver)
            self.news_urls_list = clarin_urls
            self.news_titles = clarin_titles
        else:
            print('ok')

    def set_lanacion_urls(self):
        """
        Sets the variable news_urls_list to a list with all the article URLs in the LA NACION newspaper
        Returns the list with all urls
        Checks against blacklist to ignore URLs that do not link to articles
        """
        if not self.news_urls_list:
            webdriver = driver(self.url)
            lanacion_titles, lanacion_urls = set_lanacion_titles_urls(webdriver)
            self.news_urls_list = lanacion_urls
            self.news_titles = lanacion_titles
        else:
            pass

    def set_infobae_titles_opt(self):
        """
        Checks if the URLs list is populated, if not it runs the URL getter method to get it populated
        Retrieves article title from HTML soup
        Drop duplicates
        """
        if not self.news_urls_list:
            self.set_infobae_urls_opt()
        if not self.news_titles:
            body = self.soup.find('body')
            headline_elems = body.find_all('div', {'class': 'headline normal normal-style'})
            headline_elems.extend(body.find_all('div', {'class': 'headline small normal-style'}))
            headline_elems.extend(body.find_all('div', {'class': 'headline x-large normal-style'}))
            headline_elems.extend(body.find_all('div', {'class': 'headline huge normal-style'}))
            headline_elems.extend(body.find_all('div', {'class': 'headline xx-large normal-style'}))
            headline_elems.extend(body.find_all('div', {'class': 'headline x-small normal-style'}))
            for element in headline_elems:
                news_headline = element.find('a').get_text()
                self.news_titles.append(news_headline)
        else:
            pass

    def set_infobae_titles(self):
        """
        ---- DEPRECATED -----
        Checks if the URLs list is populated, if not it runs the URL getter method to get it populated
        Access each article URL and gets the article title
        """
        print('Tset_infobae_titles() has been deprecated please use set_infobae_titles_opt() instead')
        failed_urls = []
        if not self.news_urls_list:
            self.set_infobae_urls()
            for url in self.news_urls_list:
                r_url = requests.get(url)
                url_soup = BeautifulSoup(r_url.text, 'html.parser')
                body = url_soup.find('body')
                try:
                    if body.find('h1').text:
                        news_headline = body.find('h1').text
                        news_headline = str(news_headline).strip()
                        self.news_titles.append(news_headline)
                    else:
                        failed_urls.append(url)
                except AttributeError:
                    failed_urls.append(url)

        else:
            for url in self.news_urls_list:
                r_url = requests.get(url)
                url_soup = BeautifulSoup(r_url.text, 'html.parser')
                body = url_soup.find('body')
                try:
                    if body.find('h1').text:
                        news_headline = body.find('h1').text
                        news_headline = str(news_headline).strip()
                        self.news_titles.append(news_headline)
                    else:
                        failed_urls.append(url)
                except AttributeError:
                    failed_urls.append(url)
        self.news_urls_list = [url for url in self.news_urls_list if url not in failed_urls]

    def set_minutouno_titles(self):
        """
        Checks if the URLs list is populated, if not it runs the URL getter method to get it populated
        Access each article URL and gets the article title
        """
        if not self.news_urls_list:
            # Si no estan seteadas las URLS, las seteo.
            self.set_minutouno_urls()
            body = self.soup.find("body")
            for sc in body("script"):
                sc.decompose()

            headlines = body.find_all("h2", {"class": "title"})
            for x in headlines:
                prueba = x.find('a', href=True)
                if x.find('a') == None:
                    pass
                else:
                    try:
                        urls = x.find("a").attrs['href']
                        titulos = x.find("a").get_text()
                        self.news_titles.append(titulos)
                    except:
                        pass

    def set_p12_titles_opt(self):
        """
          Checks if the URLs list is populated, if not it runs the URL getter method to get it populated
          Retrieves article title from HTML soup
        """
        if not self.news_urls_list:
            self.set_p12_urls()
        div = self.soup.find_all('div', {'class': 'article-title'})
        for item in div:
            if 'https://www.pagina12.com.ar' in item.find('a').attrs['href']:
                if any(x in item.find('a').attrs['href'] for x in blacklist_p12):
                    pass
                else:
                    news_title = item.get_text(separator=' ')
                    self.news_titles.append(news_title)

    def set_p12_titles(self):
        """
        ------ DEPRECATED ----
            Checks if the URLs list is populated, if not it runs the URL getter method to get it populated
            Access each article URL and gets the article title
        """
        print('set_p12_titles() has been deprecated, please use set_p12_titles_opt() instead()')
        failed_urls = []
        if not self.news_urls_list:
            self.set_p12_urls()
            for url in self.news_urls_list:
                r_url = requests.get(url)
                url_soup = BeautifulSoup(r_url.text, 'html.parser')
                try:
                    if url_soup.find('div', {'class': 'article-titles'}).text:
                        a = url_soup.find('div', {'class': 'article-titles'})
                        article_title = a.find('h1').string
                        news_headline = article_title
                        self.news_titles.append(news_headline)
                    else:
                        failed_urls.append(url)
                except AttributeError:
                    failed_urls.append(url)

        else:
            for url in self.news_urls_list:
                r_url = requests.get(url)
                url_soup = BeautifulSoup(r_url.text, 'html.parser')
                try:
                    if url_soup.find('div', {'class': 'article-titles'}).text:
                        a = url_soup.find('div', {'class': 'article-titles'})
                        article_title = a.find('h1').string
                        news_headline = article_title
                        self.news_titles.append(news_headline)
                    else:
                        failed_urls.append(url)
                except AttributeError:
                    failed_urls.append(url)
        self.news_urls_list = [url for url in self.news_urls_list if url not in failed_urls]

    def set_tn_titles(self):
        """
              Checks if the URLs list is populated, if not it runs the URL getter method to get it populated
              Access each article URL and gets the article title
              """
        if not self.news_urls_list:
            self.set_tn_urls()
        if not self.news_titles:
            body = self.soup.find('body', {'class': 'page--cover-tn'})
            list_page_cover = body.find_all('h2', {'class': 'article-brick__title'})
            for element in list_page_cover:
                title = element.find('a').attrs['title']
                self.news_titles.append(title)
        else:
            pass

    def set_litoral_titles(self):
        """
        Checks if the URLs list is populated, if not it runs the URL getter method to get it populated
        Access each article URL and gets the article title
        """
        if not self.news_urls_list:
            self.set_litoral_urls()
        if not self.news_titles:
            h1 = self.soup.find_all('h1', {'class': 'um_titulo entry-title'})
            for header in h1:
                news_title = header.find('a').string
                self.news_titles.append(news_title)
        else:
            pass

    def set_clarin_titles(self):
        """
        Checks if the URLs list is populated, if not it runs the URL getter method to get it populated
        Access each article URL and gets the article title
        """
        if not self.news_urls_list:
            self.set_clarin_urls()
        if not self.news_titles:
            self.news_titles = clarin_titles
        else:
            pass

    def set_lanacion_titles(self):
        """
        Checks if the URLs list is populated, if not it runs the URL getter method to get it populated
        Access each article URL and gets the article title
        """
        if not self.news_urls_list:
            self.set_lanacion_urls()
        if not self.news_titles:
            webdriver = driver(self.url)
            lanacion_titles, lanacion_urls = set_lanacion_titles_urls(webdriver)
            self.news_urls_list = lanacion_urls
            self.news_titles = lanacion_titles
        else:
            pass

    def titles_word_ranking(self):
        if not self.most_common_words:
            words = concatenate_list_data(self.news_titles)
            words = words.split()
            words = [word.lower() for word in words]
            words = [word.strip() for word in words]
            words = [word.strip(',') for word in words]
            words = [word.strip(':') for word in words]
            words = [word.strip('"') for word in words]
            words = [word.strip('“') for word in words]
            words = [word.strip('”') for word in words]
            words = [word.strip('¿') for word in words]
            words = [word.strip('?') for word in words]
            words = [word.strip('!') for word in words]
            most_common_words = Counter(words).most_common()
            self.most_common_words = most_common_words
            return self.most_common_words
        else:
            return self.most_common_words


class Article:
    def __init__(self, article_url):
        self.url = article_url
        self.r = requests.get(self.url)
        self.soup = BeautifulSoup(self.r.text, 'html.parser')
        self.newspaper_name = article_url[article_url.find('www.') + 4:article_url.find('.com')]
        self.headline = []
        self.body = []
        self.author = []
        self.publication_date = []
        self.category = []
        self.common_words = []

    def get_headline(self):

        if self.newspaper_name == 'infobae':
            self.get_infobae_headline()
            return self.headline

        elif self.newspaper_name == 'pagina12':
            self.get_p12_headline()
            return self.headline

    def get_body(self):
        # INFOBAE
        if self.newspaper_name == 'infobae':
            self.get_article_body_infobae()
            return self.body
        # PAGINA 12
        elif self.newspaper_name == 'pagina12':
            self.get_article_body_p12()
            return self.body

    def get_author(self):
        if self.newspaper_name == 'pagina12':
            author = self.soup.find('div', {'class': 'article-author'}).text
            self.author = author.replace('Por ', '')
            return self.author
        elif self.newspaper_name == 'infobae':
            if self.soup.find('a', {'class': 'author-name'}) is not None:
                author = self.soup.find('a', {'class': 'author-name'}).text
                self.author = author.replace('Por ', '')
            else:
                self.author = 'Nombre no explicito en el HTML, buscar en el articulo'
            return self.author

    def get_publication_date(self):
        if self.newspaper_name == 'infobae':
            self.publication_date = dt.datetime.strptime(str(self.soup.find(attrs={'class': 'byline - date'}).text),
                                                         '%d/%m/%Y')
            return self.publication_date

        elif self.newspaper_name == 'pagina12':
            self.publication_date = self.soup.find(attrs={'pubdate': 'pubdate'}).attrs['datetime']
            return self.publication_date

    def get_category(self):
        if self.newspaper_name == 'infobae':
            self.category = self.soup.find('div', {'class': 'header-label'}).text.strip()
            return self.category
        elif self.newspaper_name == 'pagina12':
            self.category = self.soup.find('div', {'class': 'suplement'}).text.strip()
            return self.category

    def get_article_body_infobae(self):
        article_str = ''
        if self.newspaper_name == 'infobae':
            body = self.soup.find('body')
            news_bodies = body.find_all('p', {'class': 'element element-paragraph'})

            for par in news_bodies:
                text = str(par.text)
                article_str = article_str + text
            self.body = article_str

    def get_article_body_p12(self):
        article_str = ''
        news_bodies = self.soup.find_all('div', {'class': 'article-text'})
        for par in news_bodies:
            text = str(par.text)
            article_str = article_str + text
        self.body = article_str

    def get_infobae_headline(self):
        body = self.soup.find('body')

        if body.find('h1').text:
            self.headline = body.find('h1').text
            self.headline = str(self.headline).strip()
        else:
            self.headline = 'Vacio'

    def get_p12_headline(self):
        body = self.soup.find('div', {'class': 'article-inner padding-right'})

        self.headline = body.find('h1', {'class': 'article-title'}).string
        self.headline = str(self.headline).strip()

    def extract_word_ranking(self):
        if not self.common_words:
            words_bl = ('a', 'ante', 'bajo', 'cabe', 'con', 'contra', 'de', 'desde', 'durante', 'en', 'entre', 'hacia',
                        'hasta', 'mediante', 'para', 'por', 'según', 'sin', 'so', 'sobre', 'tras', 'versus', 'vía',
                        'la', 'el', 'que', 'los', 'del', 'y', 'un', 'las', 'se', 'su', 'una', 'al', 'como', 'no',
                        'es', 'o', 'lo', 'pero', 'fue', 'mas', 'más', 'muy', 'esta', 'este', 'ha', 'está')
            words = self.body.split()
            words = [word.lower() for word in words]
            words = [word.strip(',') for word in words]
            words = [word.strip(':') for word in words]
            words = [word.strip('"') for word in words]
            words = [word.strip('') for word in words]
            common_words = Counter(words).most_common()
            self.common_words = [x for x in common_words if x[0] not in words_bl]
            return self.common_words
        else:
            return self.common_words




def concatenate_list_data(l_items):
    result = ''
    for element in l_items:
        result += (' ' + str(element))
    return result


def string_word_ranking(string):
    words_bl = ('a', 'ante', 'bajo', 'cabe', 'con', 'día', 'contra', 'me', 'después', 'dijo',
                'habló', 'sus', 'le', 'de', 'qué', 'desde', 'durante', 'en', 'entre', 'hacia',
                'hasta', 'mediante', 'para', 'por', 'según', 'sin', 'so', 'sobre', 'tras',
                'versus', 'vía', 'la', 'el', 'que', 'los', 'del', 'y', 'un', 'las', 'se',
                'su', 'una', 'al', 'como', 'no', 'es', 'o', 'lo', 'pero', 'fue', 'mas',
                'más', 'muy', 'esta', 'este', 'ha', 'está', 'cómo', 'hoy', 'así', 'ex', 'uno',
                'dos', 'tres', 'ya', 'ser', 'mil', 'mayo', 'quiénes', 'dice', 'ni')
    words = string
    words = words.split()
    words = [word.lower() for word in words]
    words = [word.strip() for word in words]
    words = [word.strip(',') for word in words]
    words = [word.strip(':') for word in words]
    words = [word.strip('"') for word in words]
    words = [word.strip('“') for word in words]
    words = [word.strip('”') for word in words]
    words = [word.strip('¿') for word in words]
    words = [word.strip('?') for word in words]
    words = [word.strip('!') for word in words]
    most_common_words = Counter(words).most_common()
    most_common_words = [x for x in most_common_words if x[0] not in words_bl]
    return most_common_words


def extract_word_ranking(headlines):
    if isinstance(headlines, list):
        words = concatenate_list_data(headlines)
        return string_word_ranking(words)

    elif isinstance(headlines, str):
        return string_word_ranking(headlines)
    else:
        print(f'Function expects a string or a list of strings got:{type(headlines)}')


def create_keyword_ranking_df(raw_dataframe, freq_threshold=3):
    """
    Outputs keyword ranking DataFrame from scraped words where frequency higher than threshold
    """
    unique_headlines = list(set(raw_dataframe.Headline))
    df = extract_word_ranking(unique_headlines)
    df = pd.DataFrame(df, columns=['keyword', 'frequency'])
    df = df[df['frequency'] >= freq_threshold]
    return df

