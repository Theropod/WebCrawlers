默认的相对路径 ./在scrapy同级
保存的csv是with bom， excel打开要without bom
pipeline有毒，jsonlin/csv都是乱码，不如用feed export
有的会有错，得加上序号来对应：column0 column1

scrapy crawl cnki_oversea -o paper_crawled.csv


