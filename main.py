# File name: main.py
# Authors: Antonio Yves de Sousa Dantas & Henrique Oliveira de Freitas
# Created on: June 19, 2021 at 3:35pm
# Last Modified on: July 04, 2021 at 11:18pm
# License: MIT
# Description: Código fonte do projeto da disciplina de Teoria da Computação
# O objetivo do projeto é realizar um Web Scrapper na página da Wikipédia
# utilizando expressões regulares para obter os dados

from wikipedia import Wikipedia # importando o objeto que representa um artigo da Wikipédia

while True:
    try:
        print("----- Web Scrapper: Wikipédia -----")

        link = input("\nInforme o link do artigo\n--->")
        artigo = Wikipedia(link)

        print("\nEbaa, o link informado está funcionando e pertence ao domínio pt.wikipedia.org!!")

        while True:
            print("\n----- Menu -----")
            print("1 - Listar o índice")
            print("2 - Listar os nomes dos arquivos de imagem")
            print("3 - Listar as referências")
            print("4 - Listar os links para outros artigos da Wikipédia")
            print("0 - Sair")
            opcao = input("Informe a opção desejada\n--->")
            # Exibe o índice do artigo informado
            if opcao == '1':
                for index in artigo.get_indice():
                    print(index)
            # Exibe o nome dos arquivos de imagem presentes no corpo do artigo
            elif opcao == '2':
                index = 1
                for img in artigo.get_images():
                    print('{}. {}'.format(index, img[0].split("src")[1].split("/")[-2]))
                    index += 1
            # Exibe as referências do artigo
            elif opcao == '3':
                index = 1
                for ref in artigo.get_referencias():
                    print('{}. {}'.format(index, ref[0].split(">")[1].split("<")[0]))
                    index += 1
            # Exibe a listagem dos links para outros artigos da Wikipédia presentes no artigo
            elif opcao == '4':
                index = 1
                for link in artigo.get_links():
                    link_formatado = link[0].split('"')
                    print(str(index) + ". " + link_formatado[3] + ": "+ "https://pt.wikipedia.org" + link_formatado[1])
                    index += 1
            # Encerra a aplicação
            elif opcao == '0':
                print("Saindoo...")
                break
            else:
                print("Oopss!! Parece que você digitou uma opção inválida :'(... Vamos tentar outra vez! ;)")
        break
    # Trata a excessão ValueError: invocada quando o usuário passa um link que não é válido
    except ValueError:
        print("\n\nOopss!! O link informado não é válido :'(\nMas não se preocupe, vamos tentar novamente! ;)\n\n")
