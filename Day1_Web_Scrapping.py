import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import display, Markdown
import google.generativeai as genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

genai.configure(api_key=api_key)

# prompt = "please provide me the comparison between AI and machine learning in a tabular format and and one chart to visualize the comparison"

# model = genai.GenerativeModel('gemini-1.5-flash')
# response = model.generate_content(prompt)
# response_text = response.text



class Website:
    url: str
    title: str
    text: str
    def __init__(self, url: str, title: str = None, text: str = None):
        self.url = url
        self.title = title
        self.text = text
        response = requests.get(url)
        print(response)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(['script', 'style', 'img', 'input']):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator=' ', strip=True)

sol = Website("https://www.geeksforgeeks.org/python/python-programming-language-tutorial/")
print(sol.url)
print(sol.title)
web_text = sol.text

prompt = f"Please summarize the following content in bullet points using proper Markdown formatting:\n\n{web_text}"

model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content(prompt)
response_text = response.text

# Format the response in Markdown with title and content
markdown_content = f"""# Website Summary

**URL:** {sol.url}
**Title:** {sol.title}

## Summary

{response_text}
"""

with open("response.txt", "w") as file:
    file.write(markdown_content)