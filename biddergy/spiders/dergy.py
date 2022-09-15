import scrapy
import pandas as pd
df = pd.read_csv('F:\Web Scraping\Golabal\keywords.csv')
base_url = 'https://www.biddergy.com/Browse?CategoryID=9&CompletedListings=false&SortFilterOptions=3&FullTextQuery={}'

class DergySpider(scrapy.Spider):
    name = 'dergy'
    def start_requests(self):
        for index in df:
            yield scrapy.Request(base_url.format(index), cb_kwargs={'index':index})

    def parse(self, response, index):
        total_pages = response.xpath("//ul[@class='pagination']/li[last()-1]/a/text()").get()
        # print(total_pages)
        current_page =response.css(".active a::text").get()
        # print(current_page)
        url = response.url

        if total_pages and current_page:
            if int(current_page) ==1:
                for i in range(1, int(total_pages)):                                                           
                    yield response.follow(url=f'{url}&page={i}', cb_kwargs={'index':index})

        links = response.css(".AuctionTitle a::attr(href)")        
        for link in links:
            yield response.follow("https://www.biddergy.com"+link.get(), callback=self.parse_item, cb_kwargs={'index':index})  
     
        
    def parse_item(self, response, index): 
        print(".................")          
        image_link = "https://www.biddergy.com/"+response.css('div.detailImages img::attr(src)').get()
        print(image_link)
        auction_date = response.css("h5.AuctionTime::text").get()
        print(auction_date)
        location = response.css("h5.AuctionLocation::text").get()
        print(location)
        product_name = response.css("h1.title::text").get()
        print(product_name)
        lot_number = response.css("h4.subtitle span::text").get()
        print(lot_number)        
        

        yield{
            
            'product_url' : response.url,           
            'item_type' :index.strip(),            
            'image_link' : image_link,          
            'auction_date' : auction_date,            
            'location' : location,           
            'product_name' : product_name,            
            'lot_id' : lot_number,          
            'auctioner' : "",
            'website' : "biddergy"            
        }