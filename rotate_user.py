import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

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

class Agent(object):
    def __init__(self, driver):
        self._driver = driver    
        self._max_try = 10    

    def get_agent(self):
        actual_agent = self._driver.execute_script("return navigator.userAgent")
        attempts = 0

        while True:
            agent = random.choice(USER_AGENT_LIST)

            if (not agent == actual_agent) or (attempts >= self._max_try):
                return agent
            
            attempts += 1

class Proxy(object):
    def __init__(self, driver):
        self._driver = driver
        self._proxies = set()

    def __del__(self):
        self._driver.close()

    def get_proxies(self, url=''):
        if url == '':
            self._driver.get('https://free-proxy-list.net/')
        else:
            self._driver.get(url)

        try:
            WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="proxylisttable_next"]/a')))
        except Exception as e:
            print('Erro ao carregar a página')
            print(e)           
            driver.close()     

        for x in range(14):
            for i in self._driver.find_elements(By.XPATH, '//*[@id="proxylisttable"]/tbody/tr'):                        
                if i.find_element(By.XPATH, './/td[7]').text == 'yes':                    
                    proxy = ":".join([i.find_element_by_xpath('.//td[1]').text, i.find_element_by_xpath('.//td[2]').text])
                    self._proxies.add(proxy)

            time.sleep(2)
            self._driver.find_element(By.XPATH, '//*[@id="proxylisttable_next"]/a').click()
        return self._proxies

    def get_random_proxy(self):
        if len(self._proxies) > 0:
            return random.choice(list(self._proxies))
        else:
            return random.choice(list(self.get_proxies()))
