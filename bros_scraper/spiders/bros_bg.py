import scrapy
import re  # Required to scrape price (only number)
from datetime import datetime  # Required to get the current date and time


class BrosBgSpider(scrapy.Spider):
    name = "bros_bg"
    start_urls = ["https://brosbg.com/klimatici-ci145"]

    # Define CSS selectors as class attributes
    CATEGORY_LINKS = "div.col-lg-4.col-md-4.col-sm-4.col-xs-6.product"
    PRODUCT_LINKS = "div.col-lg-3.col-md-4.col-sm-4.col-xs-6.product"
    PRODUCT_NAME = "div.col-lg-7.col-md-7.col-sm-7.product-single-info h1 strong::text"
    PRODUCT_CATEGORY = [
        "body > div.container-fluid > div > div > div > p > span:nth-child(3) > a > span::text",
        "body > div.container-fluid > div > div > div > p > span:nth-child(5) > a > span::text",
    ]
    PRODUCT_BRAND_NAME = "body > div.container-fluid > div > div > div > p > span:nth-child(7) > a > span::text"
    PRODUCT_PRICE = "#product-single > div.product-single > div > div.col-lg-7.col-md-7.col-sm-7.product-single-info > span > span > strong::text"
    OLD_PRICE = "#product-single > div.product-single > div > div.col-lg-7.col-md-7.col-sm-7.product-single-info > span > span > del::text"
    PRODUCT_IMAGES = "ul.slides > li"
    IMAGE_SRC = "img::attr(src)"
    NEXT_PAGE_CLICK_BUTTON = "div.pagination a:last-child::attr(href)"

    def parse(self, response):
        # Extract category links
        category_links = response.css(self.CATEGORY_LINKS).getall()
        for category_link in category_links:
            # Follow each category link
            category_response = scrapy.Selector(text=category_link)
            category_link_a = category_response.css("a::attr(href)").get()
            # Following category link to the respective page
            yield response.follow(category_link_a, callback=self.parse_category)

    def parse_category(self, response):
        product_links = response.css(self.PRODUCT_LINKS).getall()
        for product_link in product_links:
            product_link_response = scrapy.Selector(text=product_link)
            product_link_a = product_link_response.css("a::attr(href)").get()
            # Adding meta information for product link
            yield response.follow(
                product_link_a,
                callback=self.parse_product,
                meta={
                    "product_link": product_link_a
                },  # Passing the product link for later use
            )

            # Extract the URL for the next page
        next_page_url = response.css(self.NEXT_PAGE_CLICK_BUTTON).get()

        # Check if there is a next page
        if next_page_url:

            # Follow the next page link and call parse_category again
            yield scrapy.Request(next_page_url, callback=self.parse_category)

    def parse_product(self, response):
        # Retrieving product URL from meta information
        productUrl = response.meta.get("product_link")
        
        # Extracting product sku/ID
        product_sku = productUrl.split('-')[-1]

        # Extracting product name
        product_name = response.css(self.PRODUCT_NAME).get()

        # Extracting and stripping product category
        product_category = [
            response.css(selector).get() for selector in self.PRODUCT_CATEGORY
        ]

        # Extracting product brand name
        product_brand_name = response.css(self.PRODUCT_BRAND_NAME).get()

        # Extracting product price and converting to float
        product_price_with_currency = response.css(self.PRODUCT_PRICE).get()
        product_price = None
        if product_price_with_currency:
            product_price = int(re.findall(r"\d+", product_price_with_currency)[0])

        # Extracting old price if available, otherwise set to None
        old_price = response.css(self.OLD_PRICE).get()
        old_price = int(re.findall(r"\d+", old_price)[0]) if old_price else None

        # Extracting image URLs from the product page
        product_images_li_elements = response.css(self.PRODUCT_IMAGES)
        product_images = [
            li.css(self.IMAGE_SRC).get() for li in product_images_li_elements
        ]

        # Getting the current time for crawledAt field
        crawled_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Yielding the scraped data as a dictionary in JSON format
        yield {
            "productUrl": productUrl,
            "sku" : product_sku,
            "name": product_name,
            "category": product_category,
            "brand": product_brand_name,
            "price": product_price,
            "oldPrice": old_price,
            "images": product_images,
            "crawledAt": crawled_at,
        }
