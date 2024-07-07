from bs4 import BeautifulSoup
import html2text
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def getMarkdownFromResponse(soup):
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    markdown = converter.handle(soup.prettify())
    return markdown

def addUrlTitleToMarkdown(markdown, url):
    markdown = "\n___\n# URL of this part: "+url+"\n___\n\n"+markdown
    return markdown

def get_selenium_driver():
    options = Options()
    options.add_argument('--headless')  # Führt den Browser im Hintergrund aus
    options.add_argument('--disable-gpu')  # Deaktiviert die GPU-Beschleunigung, um Ressourcen zu sparen
    options.add_argument("--log-level=2")
    driver = webdriver.Chrome(options=options)  # Verwenden Sie hier den Pfad zum heruntergeladenen Webdriver
    return driver

def scrape(url):
    try:
        driver=get_selenium_driver()
        print('Scraping URL:', url)
        response = driver.get(url)
        response_selenium = driver.page_source
        soup = BeautifulSoup(response_selenium, 'html.parser')
        
        markdown = getMarkdownFromResponse(soup)
        markdown = addUrlTitleToMarkdown(markdown, url)
    except Exception as e:
        error_message = f"Error while scraping URL: {url}\n"
        error_message += f"Exception: {type(e).__name__}\n"
        markdown = error_message
    finally:
        driver.quit()
    return markdown
