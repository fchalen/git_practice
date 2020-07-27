from resources import *

## INFOBAE

# Instancio clase Newspaper con URL de infobae
infobae = Newspaper('https://www.infobae.com/?noredirect')
# Traigo las urls de infobae ( podria correr sin asignar a una variable ya que es un getter y setter)
#info_urls = infobae.get_article_urls()
# Traigo los titulares de infobae ( podria correr sin asignar a una variable ya que es un getter y setter)
#info_article_titles = infobae.get_article_titles()
# Traigo el ranking de palabras de infobae
#info_title_word_ranking = infobae.titles_word_ranking()
# Imprimo el ranking de palabras
#for word in info_title_word_ranking:
#   print(word)

# Setteo variable titulares ( seteando tmb urls por como funciona el codigo)
infobae.get_article_titles()
# Imprimo cantidad de URLs y titulares, deberian ser la misma cantidad
print('URLs en Infobae: ' + str(len(infobae.news_urls_list)))
print('Titulares en infobae: ' + str(len(infobae.news_titles)))


## PAGINA 12

# Instancio clase Newspaper con URL de infobae
pagina12 = Newspaper('https://www.pagina12.com.ar/')
# Traigo las urls de pagina 12 ( podria correr sin asignar a una variable ya que es un getter y setter)
#p12_urls = pagina12.get_article_urls()
# Traigo los titulares de pagina 12 ( podria correr sin asignar a una variable ya que es un getter y setter)
#p12_article_titles = pagina12.get_article_titles()
# Traigo el ranking de palabras de infobae
#p12_title_word_ranking = pagina12.titles_word_ranking()
# Imprimo el ranking de palabras
#for word in p12_title_word_ranking:
#    print(word)

# Setteo variable titulares ( seteando tmb urls por como funciona el codigo)
pagina12.get_article_titles()
# Imprimo cantidad de URLs y titulares, deberian ser la misma cantidad
print('URLs en Pagina12: ' + str(len(pagina12.news_urls_list)))
print('Titulares Pagina12: ' + str(len(pagina12.news_titles)))

## EL LITORAL

# Instancio clase Newspaper con URL de el litoral
litoral = Newspaper('https://www.ellitoral.com')
# Traigo las urls de el litoral ( podria correr sin asignar a una variable ya que es un getter y setter)
#lit_urls = litoral.get_article_urls()
# Traigo los titulares de el litoral ( podria correr sin asignar a una variable ya que es un getter y setter)
#lit_article_titles = litoral.get_article_titles()
# Traigo el ranking de palabras de el litoral
#lit_title_word_ranking = litoral.titles_word_ranking()
# Imprimo el ranking de palabras
#for word in lit_title_word_ranking:
#    print(word)

# Setteo variable titulares ( seteando tmb urls por como funciona el codigo)
litoral.get_article_titles()
# Imprimo cantidad de URLs y titulares, deberian ser la misma cantidad
print('URLs en El Litoral: ' + str(len(litoral.news_urls_list)))
print('Titulares El Litoral: ' + str(len(litoral.news_titles)))



## MINUTO 1

# Instancio clase Newspaper con URL de el litoral
minuto1 = Newspaper('https://www.minutouno.com/')
# Traigo las urls de el litoral ( podria correr sin asignar a una variable ya que es un getter y setter)
#min1_urls = minuto1.get_article_urls()
# Traigo los titulares de el litoral ( podria correr sin asignar a una variable ya que es un getter y setter)
#min1_article_titles = minuto1.get_article_titles()
# Traigo el ranking de palabras de el litoral
#min1_title_word_ranking = minuto1.titles_word_ranking()
# Imprimo el ranking de palabras
#for word in min1_title_word_ranking:
#    print(word)


# Setteo variable titulares ( seteando tmb urls por como funciona el codigo)
minuto1.get_article_titles()
# Imprimo cantidad de URLs y titulares, deberian ser la misma cantidad
print('URLs en Minuto 1: ' + str(len(minuto1.news_urls_list)))
print('Titulares en Minuto 1: ' + str(len(minuto1.news_titles)))


## TN

# Instancio clase Newspaper con URL de el litoral
tn = Newspaper('https://www.tn.com.ar/')
# Traigo las urls de el litoral ( podria correr sin asignar a una variable ya que es un getter y setter)
#tn_urls = tn.get_article_urls()
# Traigo los titulares de el litoral ( podria correr sin asignar a una variable ya que es un getter y setter)
#tn_article_titles = tn.get_article_titles()
# Traigo el ranking de palabras de el litoral
#tn_title_word_ranking = tn.titles_word_ranking()
# Imprimo el ranking de palabras
#for word in tn_title_word_ranking:
#    print(word)

# Setteo variable titulares ( seteando tmb urls por como funciona el codigo)
tn.get_article_titles()
# Imprimo cantidad de URLs y titulares, deberian ser la misma cantidad
print('URLs en TN: ' + str(len(tn.news_urls_list)))
print('Titulares en TN: ' + str(len(tn.news_titles)))

# CLARIN

# Instancio clase Newspaper con URL de clarin
clarin = Newspaper('https://www.clarin.com.ar/')
# Traigo las urls de clarin ( podria correr sin asignar a una variable ya que es un getter y setter)
#clarin_urls = clarin.get_article_urls()
# Traigo los titulares de clarin ( podria correr sin asignar a una variable ya que es un getter y setter)
#clarin_article_titles = clarin.get_article_titles()
# Traigo el ranking de palabras de clarin
#clarin_title_word_ranking = clarin.titles_word_ranking()
# Imprimo el ranking de palabras
#for word in tn_title_word_ranking:
#    print(word)

# Setteo variable titulares ( seteando tmb urls por como funciona el codigo)
clarin.get_article_titles()
# Imprimo cantidad de URLs y titulares, deberian ser la misma cantidad
print('URLs en Clarin: ' + str(len(clarin.news_urls_list)))
print('Titulares Clarin: ' + str(len(clarin.news_titles)))

## Ejemplos varios con la clase Article

# Instancio articulos

articulo_infobae = Article('https://www.infobae.com/america/america-latina/2019/09/12/ecuador-dejara-pasar-por-su-territorio-a-los-venezolanos-que-deseen-llegar-a-otro-pais-de-la-region/')
articulo_pagina12 = Article('https://www.pagina12.com.ar/217893-moodys-ahora-es-pesimista-con-la-argentina')

# Traigo titulo del articulo

titulo_info = articulo_infobae.get_headline()
titulo_p12 = articulo_pagina12.get_headline()

# Traigo cuerpo del articulo

cuerpo_info = articulo_infobae.get_body()
cuerpo_p12 = articulo_pagina12.get_body()