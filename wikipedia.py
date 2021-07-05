# File name: wikipedia.py
# Authors: Antonio Yves de Sousa Dantas & Henrique Oliveira de Freitas
# Created on: June 19, 2021 at 5:00pm
# Last Modified on: July 04, 2021 at 11:18pm
# License: MIT
# Description: O código abaixo fornece uma classe para representar um artigo da Wikipédia

import re # biblioteca do python para expressões regulares
import requests # biblioteca para pegar o HTML de uma página WEB
from bs4 import BeautifulSoup # biblioteca para extrair dados de uma página HTML

class Wikipedia:
    '''
    Classe que representa, de forma abstrata, um artigo da Wikipédia
    '''
    def __init__(self, link:str):
        '''
        - Construtor da classe
          - Verifica se o link informado, no momento em que o objeto foi criado, é válido
        '''
        self.link = link
        if not self.verifica_link():
            raise ValueError('O link informado não é válido!')

    def get_indice(self):
        '''
        Função para capturar o índice de um artigo da página da Wikipédia
        '''
        expressao = re.compile(r'(<span class="tocnumber">([0-9](.[0-9])*)</span> <span class="toctext">(.)+</span>)+')
        # captura todos os elementos que correspondem a expressão acima
        indice = expressao.findall(requests.get(self.link).text)
        indice_corrigido = []
        for x in indice:
            # separa o texto das tags do html que vieram com os elementos na filtragem da expressão regular
            indice_corrigido.append(x[0].split('>')[1].split('<')[0] + ' ' + x[0].split('>')[3].split('<')[0])
        return indice_corrigido
    
    def verifica_link(self):
        '''
        Função que verifica se o link informado ao instanciar o objeto é válido e corresponde a uma página da Wikipédia
        '''
        expressao = re.compile(r'(pt.wikipedia.org)')
        if expressao.search(self.link) == None: # verifica se o endereço pt.wikipedia.org faz parte do link
            return False
        # verifica se o status code da página é diferente de 200, caso seja 200 o link é válido
        elif requests.get(self.link, stream = False).status_code != 200:
            return False
        else:
            return True

    def get_links(self):
        '''
        Função que extrai todos os links para outros artigos da Wikiédia
        '''
        # pega o HTML da página
        html = requests.get(self.link).text
        # captura o conteúdo da div bodyContent que é onde fica o conteúdo do artigo
        bs_page = BeautifulSoup(html, 'html.parser').find(id="bodyContent")
        # cria a expressão regular
        expressao = re.compile(r'(<a href="/wiki/(.)+)+')
        # armazena todos os itens que correspondem a expressão
        links = expressao.findall(str(bs_page))
        return links

    def get_images(self):
        '''
        Função que extrai os nomes dos arquivos de imagem presentes no artigo
        '''
        # pega o HTML da página
        html = requests.get(self.link).text
        # captura o conteúdo da div bodyContent que é onde fica o conteúdo do artigo
        bs_page = BeautifulSoup(html, 'html.parser').find(id="bodyContent")
        # expressão para capturar a imagem que fica no inicio do artigo
        expressao_image_title = re.compile(r'(<div class="floatnone">(.)+</div>)+')
        # expressão para capturar as imagens que ficam no conteúdo do artigo
        expressao_images_body = re.compile(r'(<img (.)+ class="thumbimage" (.)+>)+')
        # concatena o resultado obtido ao executar as duas expressões regulares
        images = expressao_image_title.findall(str(bs_page)) + expressao_images_body.findall(str(bs_page))
        return images

    def get_referencias(self):
        '''
        Função que extrai as referências do artigo
        '''
        # pega o HTML da página
        html = requests.get(self.link).text
        # captura o conteúdo da div que contem a classe reflist que é onde fica as referências do artigo
        bs_page = BeautifulSoup(html, 'html.parser').find_all("div", {"class":"reflist"})
        expressao = re.compile(r'(<a class="(.)+" (.)+</a>)+')
        # armazena o resultado obtido ao executar a expressão regular
        referencias = expressao.findall(str(bs_page))
        return referencias