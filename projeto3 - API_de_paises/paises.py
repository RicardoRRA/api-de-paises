import json  # <-- Colocar primeiro imports buildin, depois os do pip e por ultimo os pacotes locais
import sys

import requests

URL_ALL = "https://restcountries.com/v3.1/all?fields=name,capital,currencies"
URL_NAME = "https://restcountries.com/v3.1/name/"


def requisicao(url):
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            return resposta.text
    except Exception as error:
        print("Erro ao fazer a requisição em:", url)
        print(error)


def parsing(texto_da_resposta):
    try:
        return json.loads(texto_da_resposta)
    except:
        print("Erro ao fazer parsing")


def contagem_de_paises():
    resposta = requisicao(URL_ALL)
    if resposta:
        lista_de_paises = parsing(resposta)
        if lista_de_paises:
            return len(lista_de_paises)


def listar_paises(lista_de_paises):
    for pais in lista_de_paises:
        print(pais["name"])


def monstrar_populacao(nome_do_pais):
    resposta = requisicao(f"{URL_NAME}{nome_do_pais}")

    if not resposta:
        print("Erro na requisição")
        return

    lista_de_paises = parsing(resposta)

    if not lista_de_paises:
        print("Pais não encontrado")
        return

    for pais in lista_de_paises:
        print("{}: {}".format(pais["name"]["common"], pais["population"]))


def mostrar_moedas(nome_do_pais):
    resposta = requisicao(f"{URL_NAME}{nome_do_pais}")

    if resposta:
        lista_de_paises = parsing(resposta)

        if lista_de_paises:
            for pais in lista_de_paises:
                print("Moedas do", pais["name"]["common"])

                moedas = pais["currencies"]

                for codigo, moeda in moedas.items():
                    print("{} - {}".format(moeda["name"], codigo))
        else:
            print("Pais não encontrado")

def ler_nome_do_pais():
    try:
        nome_do_pais = sys.argv[2]
        return nome_do_pais
    except:
        print("É preciso passar o nome do país")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("## Bem vindo ao sistema de paises ##")
        print("Uso: pyyhon paises.py <ação> <nome do pais>")
        print("Ações disponiveis: contagem, moeda, populacao")
    else:
        argumento1 = sys.argv[1]

        if argumento1 == "contagem":
            numero_de_paises = contagem_de_paises()
            print("Existem {} paises no mundo todo".format(numero_de_paises))
            exit(0)
        elif argumento1 == "moeda":
            pais = ler_nome_do_pais()
            if pais:
                mostrar_moedas(pais)
        elif argumento1 == "populacao":
            pais = ler_nome_do_pais()
            if pais:
                monstrar_populacao(pais)
        else:
            print("Argumento invalido")