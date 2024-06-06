import scrapy
import csv


class TripAdvisorAddSpider(scrapy.Spider):
    name = "tripAdvisorAddress"
    allowed_domains = ['www.tripadvisor.com']
    # start_urls = [
    #     "http://www.tripadvisor.com/Attractions-g60763-Activities-a_allAttractions.true-New_York_City_New_York.html"
    # ]
    start_urls = [
       "https://www.tripadvisor.com/Attractions-g35805-Activities-a_allAttractions.true-Chicago_Illinois.html"
    ]
    city = "Chicago"

    poiSet = set()

    with open("../../../LDA_Model_6/" + city + "DivVector.csv", 'r') as rhandle:
        spamreader = csv.reader(rhandle)

        for eachRow in spamreader:
            poiSet.add(eachRow[0])

    def parse(self, response):
        # Redirect to Detail page
        poiLinks = response.xpath('//div[@class="alPVI eNNhq PgLKC tnGGX"]/a[not(@class)]/@href').extract() # Old XPath '//a[@class="_1QKQOve4"]/@href'

        for link in poiLinks:
            # Generate absolute url link for each PoI
            poiAbsPath = response.urljoin(link)

            yield scrapy.Request(poiAbsPath, callback=self.parseAddress)

        # a - 1 ; a30 - 2; a60 - 3
        #curPage = int(response.xpath('//div[@class="pageNumbers"]/span[contains(@class, "pageNum current")]/text()').
        #              extract_first())

        curPage = response.xpath('//button[@class="BrOJk u j z _F wSSLS tIqAi iNBVo SSqtP"]//span[@class="biGQs _P ttuOS"]/text()').\
            extract_first() # Old XPath '//div[@class="pageNumbers"]/span[contains(@class, "pageNum current")]/text()'

        if curPage:
            curPage = int(curPage)
            # E.g. https://www.tripadvisor.com/Attractions-g60763-Activities-oa30
            # -a_allAttractions.true-New_York_City_New_York.html
            # preUrl = "http://www.tripadvisor.com/Attractions-g60763-Activities-oa"
            # sufUrl = "-a_allAttractions.true-New_York_City_New_York.html"

            preUrl = "https://www.tripadvisor.com/Attractions-g35805-Activities-oa"
            sufUrl = "-a_allAttractions.true-Chicago_Illinois.html"

            # nextPage = curPage + 1
            # Url: (nextPage -1) * 30 = curPage * 30

            nextPageUrl = preUrl + str(curPage * 30) + sufUrl

            # Note that URL link from "Next" button is reset in html source file, which thus cannot be directly used
            # However, we can use nextPage to check if it is the last page
            nextPage = response.xpath('//a[@aria-label="Next page"]/@href').extract() # Old XPath '//a[contains(@class, "ui_button nav next")]/@href'

            if nextPage and len(self.poiSet) > 0:
                yield scrapy.Request(nextPageUrl, callback=self.parse)

    def parseAddress(self, response):
        # Name of PoI
        poiName = response.xpath('//h1[@data-automation="mainH1"]/text()').extract_first() # Old XPath '//h1[@id="HEADING"]/text()'

        if poiName in self.poiSet:
            self.poiSet.remove(poiName)

            print(len(self.poiSet), " PoIs left...")

            # Address
            address = response.xpath('//div[@class="MJ"]/button[@class="UikNM _G B- _S _T c G_ P0 wSSLS wnNQG raEkE"]/span/text()').extract() # Old XPath '//div[@class="LjCWTZdN"]/span/text()'

            if address:
                address = address[-1]
            else:
                address = " "

            yield {
                'place':        poiName.encode("utf-8"),
                'address':      address.encode("utf-8")
            }
