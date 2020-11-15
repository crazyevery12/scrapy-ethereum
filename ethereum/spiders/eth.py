import scrapy
import json
from lxml import etree
from ethereum.items import EthereumItem

class EthSpider(scrapy.Spider):
    name = 'eth'
    allowed_domains = ['http://coinmarketcap.com/currencies/ethereum/markets/']
    start_urls = ['http://http://coinmarketcap.com/currencies/ethereum/markets//']

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
        raw = response.xpath('//div[@class="cmc-table__table-wrapper-outer"]/div/table/tbody/tr')
        for data in raw:
            items['Source'] = data.xpath('./td[2]/a/text()').get()
            items['Pair'] = data.xpath('./td[3]/a/text()').get()
            items['Price'] = data.xpath('./td[4]/div/text()').get()
            items['Volume'] = data.xpath('./td[5]/div/text()').get()
            items['Confidence'] = data.xpath('./td[6]/div/text()').get()
            items['Updated'] = data.xpath('./td[10]/div/text()').get()
        pass
