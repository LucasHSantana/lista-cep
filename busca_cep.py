from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait, Select 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time
from rotate_user import Proxy

class CEP:
    def __init__(self):
        #Inicializa o chromedriver

        #Configura as opções do navegador
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-erros')

        #Configura o caminho do chromedriver.exe
        dir_path = os.path.dirname(os.path.realpath(__file__))
        chromedriver = os.path.join(dir_path, 'chromedriver.exe')
        global driver
        driver = webdriver.Chrome(executable_path=chromedriver, options=options)

        #Abre o site dos correios
        driver.get('http://www.buscacep.correios.com.br/sistemas/buscacep/')

    def __del__(self):
        #Finaliza o chromedriver
        driver.close()

    def get_driver(self):
        return driver

    def get_cep_range(self, uf):
        #Cria uma lista com as faixas de ceps pelo estado
        pass

    def get_endereco_unico(self, cep):
        #Consulta um cep e cria um dicionário com as informações encontradas
        driver.find_element_by_link_text('Endereço por CEP').click()
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Buscar"]')))
        except Exception as e:
            print('Erro ao carregar a página')
            print(e)           
            driver.close()

        driver.find_element_by_name('CEP').send_keys(cep)
        driver.find_element_by_xpath('//input[@value="Buscar"]').click()      

        if not ('CEP NAO ENCONTRADO' in driver.page_source):
            endereco = {
                'logadouro': driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[1]').text,
                'bairro': driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[2]').text,
                'cidade': driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[3]').text.split('/')[0],
                'uf': driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[3]').text.split('/')[1],
                'cep': driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[4]').text,
            }

            return endereco
        else:
            return False

    def get_enderecos(self, faixa):
        #Consulta todos os ceps na faixa indicada
        pass

# Se for o arquivo principal...
if __name__ == '__main__':
    #Inicia o orquestrador

    #cep = CEP()
    #endereco = cep.get_endereco_unico('17204280')
    #print(endereco)
    cep = CEP()
    proxy = Proxy(cep.get_driver())
    lista = proxy.get_random_proxy()

    print(lista)
    