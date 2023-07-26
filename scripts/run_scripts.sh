#!/bin/sh
python3 src/1_search_keyword/google_ko_en.py
python3 src/1_search_keyword/keybert_ko.py
python3 src/1_search_keyword/keybert_en.py

python3 src/2_article_crawler/rss_crawler_ko.py
python3 src/2_article_crawler/rss_crawler_en.py
python3 src/2_article_crawler/article_crawler.py

python3 src/3_article_summary/bart-news.py

python3 src/4_article_keyword/keybert.py

python3 src/5_article_final/article_final.py

python3 src/6_timeline/timeline.py