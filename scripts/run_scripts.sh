#!/bin/sh
python3 src/1_search_keyword/search_keybert_kor.py
python3 src/2_article_crawler/rss_crawler.py
python3 src/2_article_crawler/article_crawler.py
python3 src/3_article_keyword/article_keybert_kor.py
python3 src/4_summarization/kobart-news.py
python3 src/5_summary_keyword/summary_keybert_kor.py
python3 src/6_evaluation/final.py
