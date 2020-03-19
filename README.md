# Web Crawlers Collection

## Puppeteer_cmip_email_crawler

### purpose

getting paper title, author, email and paper link from journals.ametsoc.org

### notes

- first getting paper title and link from search page, then follow the link to abstract information to get author and email information
- using Puppeteer framework to solve 302 redirect problems in Scrapy
- IP will be blocked after ~212 requests, using sleep time wouldn't help, considering ip rotation or distributed puppeteer instances to improve in the future
- google didn't cache the paper abstract pages, and abstract information from google search usually lacks E-mail information, therefore scraping from google is not useful this time

### usage

- required node modules: puppeteer, fs
- `node ams_email_crawler/crawler.js`
- files:
  - email_crawled.csv: example of crawled results
  - ams_email_crawler/crawler.js: the main crawler
  - ams_email_crawler/*test.js: testing file for paperinfo and search page

## Scrapy_cmip_email_crawler

### purpose

extracting paper title, author, email and paper link from journals.ametsoc.org

### notes

- same scraping workflow as puppeteer email crawler
- using Scrapy framework
- IP will be blocked after ~212 requests, and using cookies/setting sleep time/change UA won't help. After several IP blocks requests will be 302/Redirected or 403/Forbidden

### usage

- required python modules: scrapy
- `scrapy crawl ams_email`
- files:
  - crawled_emails.csv: crawled results
  - amsemailbot/amsemailbot/spiders/ams_email.py: the main crawler
  - amsemailbot/amsemailbot/items.py pipelines.py settings.py were modified

## Scrapy_cnkioversea_crawler

### purpose

extracting papaer info (abstract, title, journal, keywords) in both Chinese and English from cnki

### notes

- using url list exported from Citation information (e.g.Using NoteExpress)
- replace kns with new.oversea in url to get the english version of abstracts
- encountered Chinese encoding problem when using exporter in pipeline.py, only tails of the csv wasn't corrupted, therefore switched to feedexporter.

### usage

- required python modules: scrapy
- `rm paper_crawled.csv && scrapy crawl cnki_oversea -o paper_crawled.csv`
- files:
  - cnki_paper_urls.csv: paper abstract link
  - paper_crawled.csv: results
  - cnkioversea_crawler/spiders/cnkioversea.py: the main crawler

## ScrapyforOW

- Scrapy scripts to get player information from masteroverwatch.com and store that into mysql db
- Used packages: scrapy mysqlclient pywin32
