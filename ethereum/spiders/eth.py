import scrapy
import json
from lxml import etree
from ethereum.items import EthereumItem
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class EthSpider(scrapy.Spider):
    name = 'eth'
    allowed_domains = ['coinmarketcap.com/currencies/ethereum/markets/']
    start_urls = ['https://coinmarketcap.com/currencies/ethereum/markets/']


    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "ethereum.middlewares.RotateProxyMiddleware": 300,
            "ethereum.middlewares.RotateAgentMiddleware": 301,
            "ethereum.middlewares.EtherumMiddleware": 302
        },
        "ITEM_PIPELINES": {
            "ethereum.pipelines.EthereumPipeline": 300
        }
    }

    def parse(self, response):
        items = EthereumItem()

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(r'C:\Users\tranv\Desktop\Python Project\chromedriver.exe',chrome_options=options)
        driver.get('https://coinmarketcap.com/currencies/ethereum/markets/')

        driver.implicitly_wait(15)
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cmc-table__table-wrapper-outer")))

        # Load more data
        # driver.find_elements_by_class_name('wn9odt-0 iGNdpc cmc-button cmc-button--color-default')[0].click()

        raw = driver.find_elements_by_xpath('//div[@class="cmc-table__table-wrapper-outer"]/div/table/tbody/tr')

        for data in raw:
            items['Source'] = data.find_elements_by_xpath('.//td[2]/div/a')[0].text
            items['Pair'] = data.find_elements_by_xpath('.//td[3]/div/a')[0].text
            items['Price'] = data.find_elements_by_xpath('.//td[4]/div')[0].text
            items['Volume'] = data.find_elements_by_xpath('./td[5]/div')[0].text
            items['Confidence'] = data.find_elements_by_xpath('./td[6]/div')[0].text
            items['Updated'] = data.find_elements_by_xpath('./td[10]/div')[0].text
            yield items
        pass
