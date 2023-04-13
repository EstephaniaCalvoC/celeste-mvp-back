import requests
from bs4 import BeautifulSoup

full_url = "https://docs.galileo-ft.com/pro/docs/billpay-endpoints"

def get_hyperlinks(url):
    
    # Try to open the URL and read the HTML
    try:
        # Open the URL and read the HTML
        print("Open the URL and read the HTML")
        response = requests.get(url)
        print(url)

        # If the response is not HTML, return an empty list
        if not response.headers['Content-Type'].startswith("text/html"):
            return []

        # Decode the HTML
        html = response.content.decode('utf-8')
        print(html)
    except Exception as e:
        print(e)
        return []
    
    
if __name__ == "__main__":
    get_hyperlinks(full_url)