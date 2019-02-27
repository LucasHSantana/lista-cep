import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

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
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'    
]

#Firefox
    #'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    #'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    #'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    #'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    #'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    #'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    #'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    #'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    #'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    #'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    #'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    #'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    #'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'

MAX_TRY = 10

class RotateConnection(object):    
    def __init__(self, driver_path):            
        self._proxies = set()
        self._driver_path = driver_path
        self._driver = webdriver.Chrome(executable_path=driver_path)

        self.driver_rotator()

    def __del__(self):        
        #self._driver.close()
        pass

    def driver_rotator(self, url_callback = None):
        #Configura as opções do navegador
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

        #Configura o webdriver     
        self._driver.close()     
        self._driver = webdriver.Chrome(executable_path=self._driver_path, options=options)    

        if url_callback:
            self._driver.get(url_callback)

    def delay(self):
        time = random.randint(2, 6)
        print(f'Delay aleatório: {time}s')
        sleep(time)

    def get_driver(self):
        return self._driver

    def get_agent(self):
        actual_agent = self._driver.execute_script("return navigator.userAgent")
        attempts = 0

        while True:
            agent = random.choice(USER_AGENT_LIST)

            if (not agent == actual_agent) or (attempts >= MAX_TRY):
                return agent
            
            attempts += 1        

    def get_proxies(self, url=''):
        print('Recuperando proxies, isso pode demorar alguns minutos.')
        if url == '':
            self._driver.get('https://free-proxy-list.net/')
        else:
            self._driver.get(url)

        try:
            WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="proxylisttable_next"]/a')))
        except Exception as e:
            print('Erro ao carregar a página')
            print(e)           
            self._driver.close()     

        for x in range(4):
            for i in self._driver.find_elements(By.XPATH, '//*[@id="proxylisttable"]/tbody/tr'):                        
                if i.find_element(By.XPATH, './/td[7]').text == 'yes':                    
                    proxy = ":".join([i.find_element_by_xpath('.//td[1]').text, i.find_element_by_xpath('.//td[2]').text])
                    self._proxies.add(proxy)

            self.delay()
            self._driver.find_element(By.XPATH, '//*[@id="proxylisttable_next"]/a').click()
        return self._proxies

    def get_random_proxy(self):
        if len(self._proxies) > 0:
            return random.choice(list(self._proxies))
        else:
            return random.choice(list(self.get_proxies()))
