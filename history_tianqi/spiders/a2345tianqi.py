import re

import scrapy
from scrapy import Request

from history_tianqi.items import TianqiItem


class A2345tianqiSpider(scrapy.Spider):
    name = '2345tianqi'
    allowed_domains = ['2345.com']

    def start_requests(self):
        for year in range(2020, 2021):
            for month in range(4, 5):
                yield Request(
                    url=f"http://tianqi.2345.com/Pc/GetHistory?areaInfo%5BareaId%5D=57328&areaInfo%5BareaType%5D=2&date%5Byear%5D={year}&date%5Bmonth%5D={month}",
                    callback=self.layer_1
                )

    def layer_1(self, response):
        raw_days = re.findall("<tr>(.*?)/tr", response.text)
        list_item = []
        sub_list = []
        for raw_day in raw_days:
            item = TianqiItem()
            date = re.findall("<td>(\d*-\d*-\d*).*?/td>", raw_day)
            if not date:
                continue
            item["date"] = date[0]
            temp_max = re.findall("#ff5040.*?>(\d*).*?/td>", raw_day)
            temp_min = re.findall("#3097fd.*?>(\d*).*?/td>", raw_day)
            weather = re.findall("<td>(.*?)<.*?/td>", raw_day)[1:2]
            wind = re.findall("<td>(.*?)<.*?/td>", raw_day)[2:3]
            wind = wind[0].encode().decode("unicode-escape") if wind else ""
            wind = re.findall(".*?(\d).*?", wind)[0:1]

            if temp_max[0]:
                item["temp_max"] = temp_max[0]
            else:
                item["temp_max"] = None
                sub_list.append(len(list_item))
            item["temp_min"] = temp_min[0] if temp_min[0] else None

            item["weather"] = weather[0].encode().decode("unicode-escape") if weather else ""
            item["wind"] = wind[0] if wind else ""

            list_item.append(item)
        for item in list_item:
            for sub in sub_list:
                if sub != len(list_item) - 1:
                    list_item[sub]['temp_max'] = list_item[sub + 1]['temp_max']
                    list_item[sub]['temp_min'] = list_item[sub + 1]['temp_min']
                else:
                    list_item[sub]['temp_max'] = list_item[sub - 1]['temp_max']
                    list_item[sub]['temp_min'] = list_item[sub - 1]['temp_min']

            yield item
