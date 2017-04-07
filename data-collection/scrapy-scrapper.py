from scrapy.spiders import SitemapSpider

class BuzzFeedSpider(SitemapSpider):
	name = "buzzfeedspider"
	sitemap_urls = ['https://www.buzzfeed.com/sitemaps/en-us/sitemap_all.xml']

	def parse(self, response):
		yield { 
		"lang": response.css("html").xpath("@lang").extract_first(),
		"url": response.url
		}
