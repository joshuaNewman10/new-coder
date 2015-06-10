BOT_NAME = 'livingsocial'

SPIDER_MODULES = ['scraper_app.spiders']

DATABASE = {
  'drivername': 'postgres',
  'host': 'localhost',
  'port': '5432',
  'username': 'Jslice',
  'password': '',
  'database': 'scrape'
}

#directiory/module path to LivingSocialPipeline in pipelines.py
ITEM_PIPELINES = ['scraper_app.pipelines.LivingSocialPipeline']

