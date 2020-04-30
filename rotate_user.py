import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import socket
from selenium.webdriver.common.action_chains import ActionChains
import os

USER_AGENT_LIST = [
    #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

MAX_TRY = 10
PROXY_FILE = 'proxies.txt'

class RotateConnection(object):    
    def __init__(self, driver_path):   
        # Instancia as variáveis principais da classe         
        self._proxies = set()
        self._driver_path = driver_path        
        self._driver = webdriver.Chrome()
        
        # Pega a lista de proxy do arquivo, caso exista
        self._proxies = self.open_proxy_file()       

        # Configura o webdriver com user-agent e ip aleatórios
        self.driver_rotator()

    def __del__(self):        
        #self._driver.close()
        pass

    def driver_rotator(self, url_callback = None):        
        """
        Cada vez que essa função for executada, o desenvolvedor deve instanciar novamente
        o driver através da função 'get_driver' para evitar erros de sessão.
        """
        # Configura as opções do navegador
        agent = self.get_agent()
        proxy = self.get_random_proxy()
        
        print('Mudando configurações do driver')
        print(f'User-Agent: {agent}')
        print(f'Proxy: {proxy}')

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-erros')
        options.add_argument(f'--proxy-server={proxy}')
        options.add_argument(f"user-agent={agent}")

        # Configura o webdriver     
        if self._driver:
            self._driver.close()     
        self._driver = webdriver.Chrome(executable_path=self._driver_path, options=options)    

        # Abre a página caso seja passada como parâmetro
        if url_callback:
            self._driver.get(url_callback)

    def delay(self):
        # Gera um delay aleatório para confundir o site
        time = random.randint(2, 6)
        print(f'Delay aleatório: {time}s')
        sleep(time)

    def get_driver(self):
        # Retorna o driver configurado
        return self._driver

    def get_agent(self):        
        """
        Retorna um user-agent aleatório.
        Se o driver já estiver instanciado, retorna um user-agent diferente do atual.
        """
        actual_agent = self._driver.execute_script("return navigator.userAgent")
        attempts = 0

        while True:
            agent = random.choice(USER_AGENT_LIST)

            if (not agent == actual_agent) or (attempts >= MAX_TRY):
                return agent
            
            attempts += 1        

    def get_proxies2(self):
        # Recupera uma lista de proxies do site https://free-proxy-list.net/

        print('Recuperando proxies, isso pode demorar alguns minutos.')        
        self._driver.get('https://free-proxy-list.net/')        
        self._driver.maximize_window()

        try:
            WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="proxylisttable_next"]/a')))
        except Exception as e:
            print('Erro ao carregar a página')
            print(e)                       

        for x in range(14):
            for i in self._driver.find_elements(By.XPATH, '//*[@id="proxylisttable"]/tbody/tr'):                        
                if i.find_element(By.XPATH, './/td[7]').text == 'yes':                    
                    proxy = ":".join([i.find_element_by_xpath('.//td[1]').text, i.find_element_by_xpath('.//td[2]').text])
                    self._proxies.add(proxy)
            
            self._driver.find_element(By.XPATH, '//*[@id="proxylisttable_next"]/a').click()
        
        self.save_proxy_file()
        return self._proxies
    
    def get_proxies(self):
        # Recupera uma lista de proxies do site https://hidemyna.me/en/proxy-list/
        print('Recuperando proxies, isso pode demorar alguns minutos.')
        self._driver.get('https://hidemyna.me/en/proxy-list/')        
        self._driver.maximize_window()
        try:
            http = WebDriverWait(self._driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content-section"]/section[1]/div/div[2]/div[1]/div[2]/div[1]/label[1]/span')))            
            http.click()
            self._driver.find_element(By.XPATH, '//*[contains(@class,"pform__buttons")]/a[1]').click()    
        except Exception as e:
            print('Erro ao carregar a página')
            print(e)   

        #while True:
        for x in range(0,3): #Trocar pelo while após testes
            for row in self._driver.find_elements(By.XPATH, '//*[contains(@class, "proxy__t")]/tbody/tr'):
                ms = str(row.find_element(By.XPATH, './/td[4]/div/div/p').text).split(' ')[0]
                if int(ms) < 2500:
                    proxy = ':'.join([row.find_element(By.XPATH, './/td[1]').text, row.find_element(By.XPATH, './/td[2]').text])
                    self._proxies.add(proxy)            

            count = len(self._driver.find_elements(By.XPATH, '//*[contains(@class, "arrow__right")]'))
            if count == 0:
                break
            
            next = self._driver.find_element(By.XPATH, '//*[contains(@class, "arrow__right")]/a')            
            ActionChains(self._driver).click(next).perform()         
                    
        self.save_proxy_file()
        return self._proxies

    def get_random_proxy(self):
        # Retorna um proxy aleatório para configurar no webdriver
        while True:
            if len(self._proxies) > 0:
                proxy = random.choice(list(self._proxies))                 
            else:
                proxy = random.choice(list(self.get_proxies()))

            # Verifica se o proxy está funcionando
            if self.tcpping(proxy.split(':')[0], proxy.split(':')[1], 5):
                return proxy                          
            else:
                self._proxies.remove(proxy)

    def tcpping(self, host, port=8080, timeout=5):
        # Verifica conexão com um ip e porta específicos
        s = socket.socket()
        s.settimeout(timeout)
        try:
            s.connect((host, int(port)))
            s.close()
            return True
        except Exception:
            return False

    def save_proxy_file(self):
        # Salva a lista de proxies em um arquivo
        with open(PROXY_FILE, 'w') as f:
            for proxy in self._proxies:
                f.write(f'{proxy}\n')

    def open_proxy_file(self):
        # Recupera a lista de proxies de um arquivo
        if os.path.exists(PROXY_FILE):
            with open(PROXY_FILE, 'r') as f:            
                return set([line.strip('\n') for line in f])
        else:
            return set()

if __name__ == '__main__':  
    dir_path = os.path.dirname(os.path.realpath(__file__))
    chromedriver = os.path.join(dir_path, 'chromedriver.exe') 

    rotate = RotateConnection(chromedriver)    
    lista = rotate.open_proxy_file()
    for item in lista:
        print(item)

    print(len(lista))
