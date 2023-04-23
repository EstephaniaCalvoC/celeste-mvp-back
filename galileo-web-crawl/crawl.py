#!/usr/bin/env python3

import requests
import re
from bs4 import BeautifulSoup
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urlparse
import os
import sys


HTTP_URL_PATTERN = r'^http[s]{0,1}://(?!.*[#]).+$'


class HyperlinkParser(HTMLParser):
    
    def __init__(self):
        super().__init__()
        
        self.hyperlinks = []
        self.inside_article_tag = False
        self.skip_tag = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if self.inside_article_tag and tag == "a" and "href" in attrs and not self.skip_tag:
            self.hyperlinks.append(attrs["href"])
            return
        
        if tag == "article":
            self.inside_article_tag = True
            return
        
        if tag == "section" and "class" in attrs and attrs["class"] == "Sidebar1t2G1ZJq-vU1 rm-Sidebar hub-sidebar-content":
            self.skip_tag = True
            return
        

    def handle_endtag(self, tag):
        if tag == "section" and self.skip_tag:
            self.skip_tag = False
            
        if tag == "article":
            self.inside_article_tag = False
            
            

def get_hyperlinks(url):
    
    try:
        response = requests.get(url, timeout=60)

        if not response.headers['Content-Type'].startswith("text/html"):
            return []

        html = response.content.decode('utf-8')

    except Exception as e:
        print(url, e)
        return []

    parser = HyperlinkParser()
    parser.feed(html)

    return parser.hyperlinks


def get_clean_link(local_domain, link):
    clean_link = None

    if re.search(HTTP_URL_PATTERN, link):
        url_obj = urlparse(link)
        if url_obj.netloc == local_domain:
            clean_link = link
            
    if link.startswith("/"):
        clean_link = "https://" + local_domain + link
    
    return validate_link(clean_link) if clean_link else None


def validate_link(clean_link):
    is_valid = "edit" not in clean_link and "#" not in clean_link
    return clean_link if is_valid else None


def get_domain_hyperlinks(local_domain, url, level=1, clean_links=[], seen=set()):
    if level == 0:
        return []
    
    for full_link in set(get_hyperlinks(url)):
        link = full_link.split("#")[0]
        if link in seen:
            continue
        seen.add(link)

        
        clean_link = get_clean_link(local_domain, link)
        if clean_link:
            clean_links.append(clean_link[:-1] if clean_link.endswith("/") else clean_link)

            if level > 1:
                sub_links = get_domain_hyperlinks(local_domain, clean_link, level-1, clean_links, seen)
                for sub_link in sub_links:
                    if sub_link not in seen:
                        seen.add(sub_link)
                        clean_links.append(sub_link)

    return list(set(clean_links))


def crawl(url, all_levels = False, level=3):
    
    level = 1 if all_levels else level
    
    local_domain = urlparse(url).netloc

    bill_payment_pages = get_domain_hyperlinks(local_domain, url, level)
    bill_payment_pages.append(url)
    
    print(f'Processing: {len(bill_payment_pages)} pages. This could take a while.')
    
    queue = deque(bill_payment_pages)

    seen = set(bill_payment_pages)

    if not os.path.exists("text/"):
            os.mkdir("text/")

    if not os.path.exists("text/"+local_domain+"/"):
            os.mkdir("text/" + local_domain + "/")

    if not os.path.exists("processed"):
            os.mkdir("processed")

    while queue:

        url = queue.pop()

        with open('text/'+local_domain+'/'+url[8:].replace("/", "_") + ".txt", "w", encoding="UTF-8") as f:

            soup = BeautifulSoup(requests.get(url).text, "html.parser")

            text = soup.get_text()

            if ("You need to enable JavaScript to run this app." in text):
                print("Unable to parse page " + url + " due to JavaScript being required")
            
            f.write(text)
            
        if all_levels:
            for link in get_domain_hyperlinks(local_domain, url):
                if link not in seen:
                    queue.append(link)
                    seen.add(link)


def main():
    if len(sys.argv) < 4:
        print("Use mode: ./crawl.py full_ur: str all_levels: int[0, 1] level: int\n")
        return
    
    full_url = sys.argv[1]
    all_levels = int(sys.argv[2])
    level = int(sys.argv[3])
    
    crawl(full_url, all_levels, level)
    
     
if __name__ == "__main__":
    main()
