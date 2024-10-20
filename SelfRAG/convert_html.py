from markdownify import markdownify as md
from gpt import get_single_completion

def ai_md_cleanup(md):
    prompt = "The following markdown text is from scraping a web page. Please clean it up and remove headers, footers, and other extraneous text. \n\n" + md
    try:
        result = get_single_completion(prompt)
        if result is None:
            print("Error in ai_md_cleanup, returning original text:")
            return md
        return result
    except Exception as e:
        print("Error in ai_md_cleanup, returning original text:")
        print(e)
        return md
    
def convert_html_to_md(html_text):
    md_text = md(html_text)
    md_text = ai_md_cleanup(md_text)
    return md_text
   
        