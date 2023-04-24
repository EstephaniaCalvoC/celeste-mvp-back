#!/usr/bin/env python3

import requests
import re
from bs4 import BeautifulSoup
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urlparse
import os
import sys
from types import List


HTTP_URL_PATTERN = r'^http[s]{0,1}://(?!.*[#]).+$'


class HyperlinkParser(HTMLParser):
    """Class for parsing hyperlinks from HTML."""
    
    def __init__(self):
        super().__init__()
        
        self.hyperlinks = []
        self.inside_article_tag = False
        self.skip_tag = False

    def handle_starttag(self, tag: str, attrs: List):
        """
        Method called by the HTML parser when a start tag is encountered.
        Parses the attributes of the tag to find the href attribute and add it to the hyperlinks list.
        Also sets the inside_article_tag and skip_tag attributes if certain tags are encountered.       
        """
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
        

    def handle_endtag(self, tag: str):
        """
        Method called by the HTML parser when an end tag is encountered.
        Resets the inside_article_tag and skip_tag attributes if certain tags are encountered.
        """
        if tag == "section" and self.skip_tag:
            self.skip_tag = False
            
        if tag == "article":
            self.inside_article_tag = False
            
            
def get_hyperlinks(url: str) -> List:
    """Get all hyperlinks from a URL.
    :param url: The URL to get hyperlinks from.
    :return: A list of all the hyperlinks found in the URL.
    """
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


def get_clean_link(local_domain: str, link: str) -> str:
    """
    Format and validate the link correctly
    :param local_domain: The domain to compare the link against.
    :param link: The link to clean.
    
    :return: The cleaned link if it is valid, None otherwise.
    """
    clean_link = None

    if re.search(HTTP_URL_PATTERN, link):
        url_obj = urlparse(link)
        if url_obj.netloc == local_domain:
            clean_link = link
            
    if link.startswith("/"):
        clean_link = "https://" + local_domain + link
    
    return validate_link(clean_link) if clean_link else None


def validate_link(clean_link: str) -> str:
    """
    Run a custom validations for link
    :param clean_link: The link to validate.
    :return: The link if it is valid, None otherwise.
    """
    is_valid = "edit" not in clean_link and "#" not in clean_link
    return clean_link if is_valid else None


def get_domain_hyperlinks(local_domain: str, url: str, level: int = 1, clean_links: List = [], seen: set = set()) -> List:
    """
    Get all hyperlinks under a domain.
    :param local_domain: The domain to get hyperlinks from.
    :param url: The URL to start from.
    :param level: The number of levels to crawl.
    :param clean_links: A list of clean links found so far.
    :param seen: A set of all the links seen so far.

    :return: A list of all the clean links found.
    """
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


def crawl(url: str, all_levels: bool = False, level: int = 3) -> None:
    """
    Crawl a domain and writing the text to file.
    :param url: The starting URL for the web crawler.
    :param all_levels: Whether or not to crawl all levels of the domain.
    :param level: The number of levels to crawl.
    """
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
    """
    A web crawler for scraping text from a given URLs.
    
    Arguments:
    - full_url (str): The starting URL for the web crawler.
    - all_levels (int): If set to 1, the web crawler will crawl all levels of the domain.
    - level (int): The number of levels to crawl.
    """
    if len(sys.argv) < 4:
        print("Use mode: ./crawl.py full_ur: str all_levels: int[0, 1] level: int\n")
        return
    
    full_url = sys.argv[1]
    all_levels = int(sys.argv[2])
    level = int(sys.argv[3])
    
    crawl(full_url, all_levels, level)
    
     
if __name__ == "__main__":
    main()
