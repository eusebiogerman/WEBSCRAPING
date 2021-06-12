import unittest
import time
import sys
import os
from os import path
import traceback
import requests

from bs4 import BeautifulSoup , Comment 
from lxml import etree

#test
def newtag(bs : BeautifulSoup, tagn : str ,text: str) :
    tag = bs.new_tag(tagn)
    tag.string = text 
    return tag

def load_mlb_schedule(year):
    
    #BASE_URL = "https://www.baseball-reference.com" 
    BASE_URL = "https://www.baseball-reference.com/"
    link = f"{BASE_URL}/leagues/MLB/{year}-schedule.shtml"
    link2 = ''
    archivo = ''
    fecha = ''
    schedule = []
    gdir = str(year)
    dummycnt = 1
    
    try:
        #crear el repots
        if not (path.isdir('sessons')):
            os.mkdir('sessons')

        #carga el archivo de los datos
        #file = open("mlb_game.txt","a")

        # cargar la pagina
        time.sleep(3)
        tic = time.perf_counter()
        reps = requests.get(link)
        toc = time.perf_counter()
        
        #leer el contenido de la pagina
        html = reps.content
        if (html):  
            print(f"Schedule {toc - tic+1:0.4} seconds url: {link}")
            soup = BeautifulSoup(html,'html.parser')
            div_section_wrapper = soup.find_all('div',class_= 'section_wrapper')
            div_section_content = div_section_wrapper[0].find_all('div',class_='section_content')
            divs = div_section_content[0].find_all('div')
            for div in divs:
                ps = div.find_all('p', class_="game")
                for p in ps:
                    ems = p.find_all('em')
                    dict = {}
                    for em in ems:
                        fecha = em.a.get('href').split('/')[3][3:12]
                        archivo = f"sessons/{gdir}.txt"
                        link2 =  f"{BASE_URL}{em.a.get('href')}"
                        if dummycnt == 1 :
                           dict ={'link' : link2, 'archivo' : archivo, 'fecha' : fecha }  
                           schedule.append(dict)
                        if dummycnt % 2 == 0 :
                           dict ={'link' : link2, 'archivo' : archivo, 'fecha' : fecha }                    
                           schedule.append(dict)                     
                        dummycnt += 1   
        return schedule
    except ValueError:
            print("Error de Valor")
            traceback.print_exception(*sys.exc_info())
            return schedule
    except:    
            print("Error de general") 
            traceback.print_exception(*sys.exc_info())   
            return schedule                     


def load_mlb_games(link, archivo, gamedate):
    

    try:

        #carga el archivo de los datos
        file = open(archivo, 'a')

        # cargar la pagina
        time.sleep(3)
        tic = time.perf_counter()
        reps = requests.get(link)
        toc = time.perf_counter()
        
        #leer el contenido de la pagina
        html = reps.content
        if (html):  
            print(f"Process {toc - tic+1:0.4} seconds url: {link}")
            soup = BeautifulSoup(html,'html.parser')
           
            #codigo de los equipos
            uls = soup.find_all('ul',class_='in_list')
            teams = uls[0].find_all('a')
            home  = teams[1]['href'].split('/')[2]
            visi  = teams[2]['href'].split('/')[2]

            #saca el tag escondido
            comments = soup.find_all(text=lambda text:isinstance(text, Comment))
            htm = str([htm for htm in comments if "div_play_by_play" in htm]);
            if(htm):                          
                div = BeautifulSoup(htm,'html.parser')
                tbody  = div.find_all("tbody")
                rows = tbody[0].find_all('tr', class_ =['top_inning','bottom_inning'])
               
                for row in rows:
                    if row != ['']:
                       thtext = row.find_all('th')[0].text                     
                       row.insert(0, newtag(div,'td',thtext))
                       row.insert(0, newtag(div,'td',visi))
                       row.insert(0, newtag(div,'td',home))
                       row.insert(0, newtag(div,'td',gamedate))                     

                      # print(row)
                       cols=row.find_all('td')
                       cols=[" ".join(x.text.replace(',','|').upper().split()) for x in cols]
                       file.write(" , ".join(cols)+'\n')
                       #print(cols)  
            file.close  
    except ValueError:
            file.close 
            print("Error de Valor")
            traceback.print_exception(*sys.exc_info())
    except:    
            file.close                     
            print("Error de general") 
            traceback.print_exception(*sys.exc_info())   

#print(load_mlb_schedule(2018)) 
#score  = 'https://www.baseball-reference.com/boxes/CHN/CHN201810020.shtml'                                            
#load_mlb_games(score,2018)
                                
for score in load_mlb_schedule(2018):
    load_mlb_games(score['link'], score['archivo'], score['fecha'])
