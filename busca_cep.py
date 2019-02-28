from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait, Select 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
from rotate_user import RotateConnection

class CEP:
    def __init__(self):
        #Configura o caminho do chromedriver.exe
        dir_path = os.path.dirname(os.path.realpath(__file__))
        chromedriver = os.path.join(dir_path, 'chromedriver.exe')        
        self._rotate = RotateConnection(chromedriver)        
        self._driver = self._rotate.get_driver()

        #Abre o site dos correios        
        self._driver.get('http://www.buscacep.correios.com.br/sistemas/buscacep/')

    def __del__(self):
        #Finaliza o chromedriver
        pass         

    def rotate(self, url_callback):
        self._rotate.driver_rotator(url_callback)
        self._driver = self._rotate.get_driver()

    def get_cep_range(self, uf):
        #Cria uma lista com as faixas de ceps pelo estado
        pass

    def get_endereco_unico(self, cep):
        #Consulta um cep e cria um dicionário com as informações encontradas       

        self.rotate('http://www.buscacep.correios.com.br/sistemas/buscacep/')

        self._driver.find_element_by_link_text('Endereço por CEP').click()
        try:
            WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Buscar"]')))
        except Exception as e:
            print('Erro ao carregar a página')
            print(e)                       

        self._driver.find_element_by_name('CEP').send_keys(cep)
        self._rotate.delay()
        self._driver.find_element_by_xpath('//input[@value="Buscar"]').click()      

        if not ('CEP NAO ENCONTRADO' in self._driver.page_source):
            endereco = {
                'logadouro': self._driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[1]').text,
                'bairro': self._driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[2]').text,
                'cidade': self._driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[3]').text.split('/')[0],
                'uf': self._driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[3]').text.split('/')[1],
                'cep': self._driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/table/tbody/tr[2]/td[4]').text,
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
    end = cep.get_endereco_unico('17204280')    
    print(end)
    end = cep.get_endereco_unico('17204286')
    print(end)
