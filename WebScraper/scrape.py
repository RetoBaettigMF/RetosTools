import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
from os import system
import html2text
import re
from ai_cleanup import aiCleanup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

resultdir = 'results\\'
system('mkdir ' + resultdir)
done_urls = []
pagenumber = 1

def getMarkdownFilename(url):
    global pagenumber
    filename = url
    filename = filename.replace('http://', '')
    filename = filename.replace('https://', '')
    filename =re.sub(r'[\\/*?:"<>|]', '_', filename)
    filename = resultdir+str(pagenumber)+filename+ '.md'
    pagenumber += 1
    return filename

def responseIsHTML(response):
    if response.status_code != 200:
        print("Error: ", response.status_code)
        return False
     
    if not ('text/html' in response.headers['Content-Type']):
        return False
    
    return True

def getMarkdownFromResponse(soup):
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    markdown = converter.handle(soup.prettify())
    cleaned=aiCleanup(markdown)
    if (cleaned != None):
        markdown = cleaned
    return markdown

def writeMarkdownToFile(markdown, url):
    filename = getMarkdownFilename(url)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(markdown)

def addUrlTitleToMarkdown(markdown, url):
    markdown = "\n___\n# URL of this part: "+url+"\n___\n\n"+markdown
    return markdown

def get_base_url(url):
    parsed_url = urlparse(url)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc
    return base_url

def get_selenium_driver():
    options = Options()
    #options.add_argument('--headless')  # Führt den Browser im Hintergrund aus
    options.add_argument('--disable-gpu')  # Deaktiviert die GPU-Beschleunigung, um Ressourcen zu sparen
    driver = webdriver.Chrome(options=options)  # Verwenden Sie hier den Pfad zum heruntergeladenen Webdriver
    return driver

def scrape(driver, url, base_url, recursive=True):
    global done_urls

    if url in done_urls:
        return
    done_urls.append(url)

    print('Scraping URL:', url)
    response = driver.get(url)
    response_selenium = driver.page_source
    soup = BeautifulSoup(response_selenium, 'html.parser')
    
    markdown = getMarkdownFromResponse(soup)
    markdown = addUrlTitleToMarkdown(markdown, url)
    writeMarkdownToFile(markdown, url)
    
    # Finden Sie alle Links auf der Seite
    for link in soup.find_all('a'):
        href = link.get('href')
        
        if href == None:
            continue    

        if href.startswith('#'):
            continue

        if href.startswith('mailto:'):
            continue    

        if href.startswith('javascript:'):
            continue    

        if href.startswith('/'):
            href = get_base_url(base_url)+"/"+href[1:]
        
        if base_url in href and recursive:
            # Rufen Sie die Funktion rekursiv auf, um die verlinkte Seite zu durchsuchen
            scrape(driver, href, base_url)

# Method which concatenates all text files in the result directory into one file
def concatenateFiles(input_dir, output_filename):

    with open(output_filename, 'w', encoding='utf-8') as outfile:
        for filename in os.listdir(input_dir):
            if filename.endswith('.md'):
                with open(os.path.join(input_dir, filename), encoding='utf-8') as infile:
                    for line in infile:
                        outfile.write(line)

def main():
    MainURL = sys.argv[1]
    recursive = False
    if len(sys.argv) > 2:
        if sys.argv[2] == '--recursive':
            recursive = True
        else:
            print("Unknown parameter: ", sys.argv[2])
            exit()
    if (MainURL == None):
        print("Please provide a URL as command line parameter")
        print("Usage: python scrape.py <URL> [--recursive]")
        print("Example: python scrape.py https://example.com")
        print("Example: python scrape.py https://example.com --recursive")
        print("The optional parameter --recursive is used to scrape all subpages of the main URL recursively.")
        exit()


    driver=get_selenium_driver()
    #Erster Aufruf manuell machen, um einzuloggen und Cookies zu akzeptieren
    #scrape(driver, MainURL, MainURL, False);
    #ok = input("Please accept cookies and login if necessary. Then press enter to continue")
    #Dann den eigentlichen rekursiven Scraping-Aufruf machen
    scrape(driver, MainURL, MainURL, recursive)
    concatenateFiles(resultdir, 'result.md')
    driver.quit()

if __name__ == "__main__":
    main()