import os
from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup
import urllib.request
import random
from PIL import Image
import pandas as pd
import json
import tldextract
import cv2
import numpy as np
import tinify
from urllib.request import urlopen
from urllib.parse import urlsplit
import requests

# Create your views here.

def grades(request):
    
    if request.method == 'GET': 
        urlPesquisa = request.GET['url']
        dados = {
            'parte1' : {},
            'parte2' : {},
            'detalhes': {}
        }
        chrome_options = Options()
        chrome_options.add_argument("-headless")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        url = f'https://webspeedtest.cloudinary.com/'
        driver.get(url)
        sleep(5)

        elemento = driver.find_element_by_tag_name('input')
        elemento.send_keys(urlPesquisa)
        elemento.submit()
        sleep(65)

        score = driver.find_elements_by_class_name('grade')[0].text
        orweight = driver.find_element_by_class_name('original-images-weight').text
        traweight = driver.find_element_by_class_name('trans-images-weight').text
        values = driver.find_elements_by_class_name('value')
        screenshot = driver.find_element_by_class_name('screenshot').get_attribute('src')

        detalhes = driver.find_elements_by_class_name('resultsItem')
        for index, value in enumerate(detalhes):
           
            button = driver.find_elements_by_class_name('toggle-btn')[index]
            button.click()
            sleep(2)
            dados['detalhes'][index] = {
                'url_image' : driver.find_elements_by_class_name('image-orig > img')[index].get_attribute('src'),
                'name_image' : driver.find_elements_by_class_name('image-data-name')[index].text,
                'extension' : driver.find_elements_by_class_name('type')[index].text,
                'size' : driver.find_elements_by_class_name('bytes')[index].text,
                'percentage' : driver.find_elements_by_class_name('image-final-percent')[index].text,
                'final_pixel' : driver.find_elements_by_class_name('image-final-pixel')[index].text,
                'download' : value.find_elements_by_class_name('links > a')[0].get_attribute('href'),
            }
        
        for index, value in enumerate(values):
            dados['parte1'][index] = value.text
        dados['parte2'] = {
                'page_image_score' : score,
                'current_images' : orweight,
                'potential_after_smart_compression' : traweight,
                'url_screenshot' : screenshot
            }
        driver.quit()
        return HttpResponse(json.dumps(dados), content_type="application/json")


def cssvalidation(request):
    
    if request.method == 'GET': 
        urlPesquisa = request.GET['url']
        
        chrome_options = Options()
        chrome_options.add_argument("-headless")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        url = f'https://jigsaw.w3.org/css-validator/'
        driver.get(url)
        sleep(4)
        elemento = driver.find_element_by_tag_name('input')
        elemento.send_keys(urlPesquisa)
        elemento.submit()
        sleep(15)
        dados = {
            'errors' : {
                'title' : '',
                'info_errors' : {},
            },
            'warnings' : {
                'title' : '',
                'info_warnings' : {},
            },
            'urlComplero' : driver.current_url,
        }
        container = driver.find_element_by_id("results_container")
        errors = driver.find_elements_by_class_name('error-section')
        tagerrors = driver.find_element_by_id('errors')
        dados['errors']['title'] = tagerrors.find_element_by_tag_name('h3').text
        qt = 0
        qt2 = 0
        for index, value in enumerate(errors):
            qt = qt + 1
            if qt != 3:
                dados['errors']['info_errors'][index] = {
                    'url_css' : driver.find_elements_by_class_name('error-section > h4 > a')[index].get_attribute('href'),
                    'table' : {}
                }
                tableSearch = value.find_elements_by_class_name('error')
                for tbIndex, tbValue in enumerate(tableSearch):
                    td = tbValue.find_elements_by_tag_name('td')
                    dados['errors']['info_errors'][index]['table'][tbIndex] = {}
                    for trIndex, trValue in enumerate(td):
                        dados['errors']['info_errors'][index]['table'][tbIndex][trIndex]= trValue.text
            else:
                break

        warnings = driver.find_elements_by_class_name('warning-section')
        tagwarning = driver.find_element_by_id('warnings')
        dados['warnings']['title'] = tagwarning.find_element_by_tag_name('h3').text
        for index, value in enumerate(warnings):
            qt2 = qt2 + 1
            if qt2 != 3:
                dados['warnings']['info_warnings'][index] = {
                    'url_css' : driver.find_elements_by_class_name('warning-section > h4 > a')[index].get_attribute('href'),
                    'table' : {}
                }
                tableSearch = value.find_elements_by_class_name('warning')
                for tbIndex, tbValue in enumerate(tableSearch):
                    td = tbValue.find_elements_by_tag_name('td')
                    dados['warnings']['info_warnings'][index]['table'][tbIndex] = {}
                    for trIndex, trValue in enumerate(td):
                        dados['warnings']['info_warnings'][index]['table'][tbIndex][trIndex]= trValue.text
            else:
                break

        # score = driver.find_elements_by_class_name('grade')[0].text
        # orweight = driver.find_element_by_class_name('original-images-weight').text
        # traweight = driver.find_element_by_class_name('trans-images-weight').text
        # values = driver.find_elements_by_class_name('value')
        # screenshot = driver.find_element_by_class_name('screenshot').get_attribute('src')

        # detalhes = driver.find_elements_by_class_name('resultsItem')
        # for index, value in enumerate(detalhes):
        #     button = driver.find_elements_by_class_name('toggle-btn')[index].click
        #     dados['detalhes'][index] = {
        #         'url_image' : driver.find_elements_by_class_name('image-orig > img')[index].get_attribute('src'),
        #         'name_image' : driver.find_elements_by_class_name('image-data-name')[index].text,
        #         'extension' : driver.find_elements_by_class_name('type')[index].text,
        #         'size' : driver.find_elements_by_class_name('bytes')[index].text,
        #         'percentage' : driver.find_elements_by_class_name('image-final-percent')[index].text,
        #         'final_pixel' : driver.find_elements_by_class_name('image-final-pixel')[index].text,
        #         'download' : driver.find_elements_by_class_name('links > a')[index].get_attribute('href'),
        #     }
        
        # for index, value in enumerate(values):
        #     dados['parte1'][index] = value.text
        # dados['parte2'] = {
        #         'page_image_score' : score,
        #         'current_images' : orweight,
        #         'potential_after_smart_compression' : traweight,
        #         'url_screenshot' : screenshot
        #     }
        # driver.quit()
        driver.quit()
        return HttpResponse(json.dumps(dados), content_type="application/json")

def keyworddensity(request):
    
    if request.method == 'GET': 
        dados = {
            'KA' : {},
            'word' : {},
            
            
        }

        urlGet = request.GET['url']
        keyword = request.GET['keyword']
        chrome_options = Options()
        chrome_options.add_argument("-headless")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        url = f'https://www.zippy.co.uk/keyworddensity/'
        driver.get(url)
        sleep(4)

        elemento = driver.find_element_by_id("url")
        elemento.send_keys(urlGet)

        elemento2 = driver.find_element_by_id("keyword")
        elemento2.send_keys(keyword)

        elemento3 = driver.find_element_by_id("check-now")
        elemento3.click()

        sleep(2)
        if keyword != '':
            kaAll = driver.find_elements_by_class_name('seeall > a')[2]
            kaAll.click()

            kaAll = driver.find_elements_by_class_name('seeall > a')[0]
            kaAll.click()

            divTabela = driver.find_element_by_id("keyword_result")
            html_content_div = divTabela.get_attribute('outerHTML')

            soup = BeautifulSoup(html_content_div, 'html.parser')
            table = soup.find(name='table')

            df_full = pd.read_html(str(table))[0]

            dados['KA'] = df_full.to_dict('records')

        botao = driver.find_elements_by_class_name('clearfix > li')[0]
        botao.click()

        kaAll = driver.find_elements_by_class_name('seeall > a')[0]
        kaAll.click()

        divTabela = driver.find_element_by_id("phase_1")
        html_content_div = divTabela.get_attribute('outerHTML')

        soup = BeautifulSoup(html_content_div, 'html.parser')
        table = soup.find(name='table')

        df_full = pd.read_html(str(table))[0]

        dados['word'][0] = {
            'name' : 'One Word',
            'itens' : df_full.to_dict('records')
        }

        divTabela = driver.find_element_by_id("phase_2")
        html_content_div = divTabela.get_attribute('outerHTML')

        soup = BeautifulSoup(html_content_div, 'html.parser')
        table = soup.find(name='table')

        df_full = pd.read_html(str(table))[0]

        dados['word'][1] = {
            'name' : 'Two Word Phrases',
            'itens' : df_full.to_dict('records')
        }

        divTabela = driver.find_element_by_id("phase_3")
        html_content_div = divTabela.get_attribute('outerHTML')

        soup = BeautifulSoup(html_content_div, 'html.parser')
        table = soup.find(name='table')

        df_full = pd.read_html(str(table))[0]


        dados['word'][2] = {
            'name' : 'Three Word Phrases',
            'itens' : df_full.to_dict('records')
        }

        divTabela = driver.find_element_by_id("phase_4")
        html_content_div = divTabela.get_attribute('outerHTML')

        soup = BeautifulSoup(html_content_div, 'html.parser')
        table = soup.find(name='table')

        df_full = pd.read_html(str(table))[0]


        dados['word'][3] = {
            'name' : 'Four Word Phrases',
            'itens' : df_full.to_dict('records')
        }
        
        

       
        # container = driver.find_element_by_id("results_container")
        # errors = driver.find_elements_by_class_name('error-section')
        # tagerrors = driver.find_element_by_id('errors')
        # dados['errors']['title'] = tagerrors.find_element_by_tag_name('h3').text
        # qt = 0
        # qt2 = 0
        # for index, value in enumerate(errors):
        #     qt = qt + 1
        #     if qt != 3:
        #         dados['errors']['info_errors'][index] = {
        #             'url_css' : driver.find_elements_by_class_name('error-section > h4 > a')[index].get_attribute('href'),
        #             'table' : {}
        #         }
        #         tableSearch = value.find_elements_by_class_name('error')
        #         for tbIndex, tbValue in enumerate(tableSearch):
        #             td = tbValue.find_elements_by_tag_name('td')
        #             dados['errors']['info_errors'][index]['table'][tbIndex] = {}
        #             for trIndex, trValue in enumerate(td):
        #                 dados['errors']['info_errors'][index]['table'][tbIndex][trIndex]= trValue.text
        #     else:
        #         break

        # warnings = driver.find_elements_by_class_name('warning-section')
        # tagwarning = driver.find_element_by_id('warnings')
        # dados['warnings']['title'] = tagwarning.find_element_by_tag_name('h3').text
        # for index, value in enumerate(warnings):
        #     qt2 = qt2 + 1
        #     if qt2 != 3:
        #         dados['warnings']['info_warnings'][index] = {
        #             'url_css' : driver.find_elements_by_class_name('warning-section > h4 > a')[index].get_attribute('href'),
        #             'table' : {}
        #         }
        #         tableSearch = value.find_elements_by_class_name('warning')
        #         for tbIndex, tbValue in enumerate(tableSearch):
        #             td = tbValue.find_elements_by_tag_name('td')
        #             dados['warnings']['info_warnings'][index]['table'][tbIndex] = {}
        #             for trIndex, trValue in enumerate(td):
        #                 dados['warnings']['info_warnings'][index]['table'][tbIndex][trIndex]= trValue.text
        #     else:
        #         break

        # score = driver.find_elements_by_class_name('grade')[0].text
        # orweight = driver.find_element_by_class_name('original-images-weight').text
        # traweight = driver.find_element_by_class_name('trans-images-weight').text
        # values = driver.find_elements_by_class_name('value')
        # screenshot = driver.find_element_by_class_name('screenshot').get_attribute('src')

        # detalhes = driver.find_elements_by_class_name('resultsItem')
        # for index, value in enumerate(detalhes):
        #     button = driver.find_elements_by_class_name('toggle-btn')[index].click
        #     dados['detalhes'][index] = {
        #         'url_image' : driver.find_elements_by_class_name('image-orig > img')[index].get_attribute('src'),
        #         'name_image' : driver.find_elements_by_class_name('image-data-name')[index].text,
        #         'extension' : driver.find_elements_by_class_name('type')[index].text,
        #         'size' : driver.find_elements_by_class_name('bytes')[index].text,
        #         'percentage' : driver.find_elements_by_class_name('image-final-percent')[index].text,
        #         'final_pixel' : driver.find_elements_by_class_name('image-final-pixel')[index].text,
        #         'download' : driver.find_elements_by_class_name('links > a')[index].get_attribute('href'),
        #     }
        
        # for index, value in enumerate(values):
        #     dados['parte1'][index] = value.text
        # dados['parte2'] = {
        #         'page_image_score' : score,
        #         'current_images' : orweight,
        #         'potential_after_smart_compression' : traweight,
        #         'url_screenshot' : screenshot
        #     }
        # driver.quit()
        driver.quit()
        return HttpResponse(json.dumps(dados), content_type="application/json")

def imageanalysis(request):
    dados = {
            'parte1' : {},
            'parte2' : {},
            'detalhes': {}
        }
    # request = requests.get("http://127.0.0.1:9000/api/gettokenvalido")
    # todos = json.loads(request.content)
    # tinify.key = todos['token']
    # source = tinify.from_file("E:/django/seotools/seotools/grades/result.png")
    # source.to_file("optimized.png")

    # Save the transparency channel alpha
    # b,g,r = cv2.split(src)


    # # ... Your image processing

    # # Duplicate the grayscale image to mimic the BGR image and finally add the transparency
    # img = cv2.merge((b,g,r))
    # cv2.imwrite("result.png", img)
    # urlSize = urllib.request.urlopen('https://res.cloudinary.com/webspeedtest/image/upload/c_limit,dpr_auto,h_300,w_400/cemf82fswojrzzpgdo5c')
    # sizeAntigo = len(urlSize.read())
    # urllib.request.urlretrieve('https://res.cloudinary.com/webspeedtest/image/upload/c_limit,dpr_auto,h_300,w_400/cemf82fswojrzzpgdo5c', "file_name")
    
    # imagem = Image.open("file_name").convert('RGB')
    # with imagem as img:
    #     width, height = img.size
    # redimensionada = imagem.resize((width, height))
    # urlpath = 'E:/seotools/public/django/'
    # aleatoriopath = str(random.randint(737123673, 992882918828))
    # aleatorioimage = str(random.randint(737123673, 992882918828))
    # os.mkdir(urlpath + aleatoriopath)
    # novopath = urlpath + aleatoriopath
    # nome_sem_ext = aleatorioimage + '.jpg'
    # redimensionada.save(os.path.join(novopath, nome_sem_ext))
    # sizeNovo = os.path.getsize(novopath +'/'+ nome_sem_ext)
    
    
    if request.method == 'GET': 
        url = request.GET['url']
        urlConfirm = tldextract.extract(url)
        domain = urlConfirm.domain
        qtpag = int(request.GET['qtpag'])
        SearchUrlVerificadas = []
        SearchUrlNaoVerificadas = []
        SearchUrlConferidas = []
        chrome_options = Options()
        chrome_options.add_argument("-headless")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        # url = f'https://jigsaw.w3.org/css-validator/'
        driver.get(url)
        sleep(2)
        SearchUrlNaoVerificadas.append(driver.current_url)
        links = driver.find_elements_by_tag_name('a')
        print('url'+url)
        for index, value in enumerate(links):
            if not (value.get_attribute('href') in SearchUrlNaoVerificadas):
                if str(value.get_attribute('href')).count(str(domain)) == 1:
                    print('url = '+str(value.get_attribute('href'))+'contem a palava'+str(domain))
                    if len(SearchUrlNaoVerificadas) < qtpag:
                        SearchUrlNaoVerificadas.append(value.get_attribute('href'))
               

        for index, value in enumerate(SearchUrlNaoVerificadas):
            print('len'+str(len(SearchUrlNaoVerificadas)))
            print('peixoto value'+str(index)+'-'+value)
            driver.get(value)
            sleep(1)
            print('peixoto'+str(index)+'-'+driver.current_url)
            request = requests.get(driver.current_url)
            if request.status_code >= 200 and request.status_code <= 299:
                SearchUrlConferidas.append(driver.current_url)
        
        SearchUrlNaoVerificadas = SearchUrlConferidas
        SearchUrlConferidas = []
        
        while len(SearchUrlNaoVerificadas) != 0:
            SearchUrlVerificadas.append(SearchUrlNaoVerificadas[0])
            try:
                driver.get(SearchUrlNaoVerificadas[0])
                links = driver.find_elements_by_tag_name('a')
                SearchUrlNaoVerificadas.pop(0)
                for index, value in enumerate(links):
                    if not (value.get_attribute('href') in SearchUrlNaoVerificadas):
                        if not (value.get_attribute('href') in SearchUrlVerificadas):
                            if str(value.get_attribute('href')).count(str(domain)) == 1:
                                if (len(SearchUrlVerificadas) + len(SearchUrlNaoVerificadas) != qtpag):
                                    SearchUrlNaoVerificadas.append(value.get_attribute('href'))
                                else: 
                                    break
            except:
                SearchUrlNaoVerificadas.pop(0)

        for index, value in enumerate(SearchUrlVerificadas):
            driver.get(value)
            request = requests.get(driver.current_url)
            print('peixoto2'+str(index)+'-'+driver.current_url)
            if request.status_code >= 200 and request.status_code <= 299:
                SearchUrlConferidas.append(driver.current_url)

        SearchUrlVerificadas = SearchUrlConferidas

        for index, value in enumerate(SearchUrlVerificadas):
            try:
                driver.get(value)
                dados['detalhes'][index] = {
                    'urlPrincipal' : value,
                    'images' : {}
                }
                imagesAll = driver.find_elements_by_tag_name('img')
                urlpath = 'E:/django/seotools/assets/'
                aleatoriopath = str(random.randint(737123673, 992882918828))
                os.mkdir(urlpath + aleatoriopath)
                imgerror = 0
                for index2, value2 in enumerate(imagesAll):
                    if ('http' in str(value2.get_attribute('src'))):
                        if ('png' in str(value2.get_attribute('src'))) or ('jpg' in str(value2.get_attribute('src'))) or ('jpeg' in str(value2.get_attribute('src'))):
                            try:
                                request = requests.get("https://seo.kqc.ca/api/gettokenvalido")
                                todos = json.loads(request.content)
                                tinify.key = todos['token']
                                source = tinify.from_url(value2.get_attribute('src'))
                                
                                # urlSize = urllib.request.urlopen(value2.get_attribute('src'))
                                # ext = 'png'
                                # if ('png' in str(value2.get_attribute('src'))):
                                #     ext = 'png'
                                # else:
                                #     ext = 'png'
                                # sizeAntigo = len(urlSize.read())
                                # urllib.request.urlretrieve(value2.get_attribute('src'), "file_name")
                                
                                # imagem = Image.open("file_name").convert('RGB')
                                # with imagem as img:
                                #     width, height = img.size
                                # # redimensionada = imagem.resize((width, height), Image.ANTIALIAS)
                                url = value2.get_attribute('src')

                                parts = urlsplit(url)
                                paths = parts.path.split('/')

                                extArray = urlsplit(paths[-1])
                                extArray = parts.path.split('.')
                                
                                aleatorioimage = str(random.randint(737123673, 992882918828))
                                
                                novopath = urlpath + aleatoriopath
                                nome_sem_ext = aleatorioimage + paths[-1]
                                source.to_file(os.path.join(novopath +'/'+ nome_sem_ext))
                                urlDownload = aleatoriopath +'/'+nome_sem_ext
                                
                                dados['detalhes'][index]['images'][index2] = {
                                    'url_image' : value2.get_attribute('src'),
                                    'name_image' : paths[-1],
                                    'extension' : extArray[-1],
                                    'size' : '',
                                    'percentage' : '',
                                    'final_pixel' : '',
                                    'download' : urlDownload,
                                }
                            except:
                                imgerror = imgerror + 1
                    
            except ValueError:
                SearchUrlNaoVerificadas.pop(0)
            
        # for index, value in enumerate(SearchUrl):
        #     driver.get(value)
        #     sleep(2)
        #     links = driver.find_elements_by_tag_name('a')
        #     for index, value in enumerate(links):
        #     if not (value.get_attribute('href') in SearchUrl):
        #         if (str(url) in str(value.get_attribute('href'))):
        #             SearchUrl.append(value.get_attribute('href'))
        driver.quit()   
        return HttpResponse(json.dumps(dados), content_type="application/json")
    # return HttpResponse('ok')

def url_to_image(url, readFlag=cv2.IMREAD_COLOR):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, readFlag)

    # return the image
    return image

def hostgator(request):
    
    if request.method == 'GET': 

        # chrome_options = Options()
        # chrome_options.add_argument("-headless")
        # driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
        driver = webdriver.Chrome(ChromeDriverManager().install())
        url = f'https://financeiro.hostgator.com.br/'
        driver.get(url)
        sleep(10)
       
        elemento3 = driver.find_element_by_id('cookie-cta')
        elemento3.click()

        elemento3 = driver.find_element_by_class_name('recaptcha-checkbox-border').click()

        sleep(30)

def ourocred(request):
    dados = {
            'itens' : {}
        }
    if request.method == 'GET': 

        # chrome_options = Options()
        # chrome_options.add_argument("-headless")
        # driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
        driver = webdriver.Chrome(ChromeDriverManager().install())
        url = f'http://127.0.0.1:9000/planilha'
        driver.get(url)

        tr = driver.find_elements_by_tag_name('tr')

        divTabela = driver.find_element_by_tag_name("body")
        html_content_div = divTabela.get_attribute('outerHTML')

        soup = BeautifulSoup(html_content_div, 'html.parser')
        table = soup.find(name='table')

        df_full = pd.read_html(str(table))[0]
        dados['itens'] = df_full.to_dict('records')

      
        
    return HttpResponse(json.dumps(dados), content_type="application/json")

def adv(request):
    dados = {
            'itens' : {}
        }
    if request.method == 'GET': 

        # chrome_options = Options()
        # chrome_options.add_argument("-headless")
        # driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
        driver = webdriver.Chrome(ChromeDriverManager().install())
        url = f'https://www.promobank.com.br/'
        driver.get(url)
        sleep(1)

        elemento = driver.find_element_by_id("loginEmpresa")
        elemento.send_keys('2216')

        elemento2 = driver.find_element_by_id("loginUsuario")
        elemento2.send_keys('ourocred')

        elemento3 = driver.find_element_by_id("loginSenha")
        elemento3.send_keys('102030')

        elemento4 = driver.find_element_by_id("submitButton")
        elemento4.click()

        sleep(40)
        
        elemento5 = driver.find_element_by_id("bSairTopo")
        elemento5.click()
        

        sleep(30)



      
        
    return HttpResponse(json.dumps(dados), content_type="application/json")

def ole(request):
    dados = {
            'itens' : {}
        }
    if request.method == 'GET': 

        # chrome_options = Options()
        # chrome_options.add_argument("-headless")
        # driver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
        driver = webdriver.Chrome(ChromeDriverManager().install())
        url = f'https://ola.oleconsignado.com.br/'
        driver.get(url)
        sleep(1)

        elemento = driver.find_element_by_id("Login")
        elemento.send_keys('FABIO.BA')

        elemento2 = driver.find_element_by_id("Senha")
        elemento2.send_keys('2022Banco')

        # elemento3 = driver.find_element_by_id("loginSenha")
        # elemento3.send_keys('102030')

        elemento4 = driver.find_element_by_id("botaoAcessar")
        elemento4.click()
        

        sleep(30)



      
        
    return HttpResponse(json.dumps(dados), content_type="application/json")
       
       
