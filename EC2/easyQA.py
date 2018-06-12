from module import module
import urllib
from lxml import html
import requests
class easyQA(module):
    def __init__(self):
        super().__init__()
    def response(self,text,context):
        query = urllib.parse.quote(text)
        link = urllib.parse.urljoin('https://www.evi.com/q/',query)
        page = requests.get(link)
        tree = html.fromstring(page.content)
        response =  tree.xpath('//div[@class="tk_common"]/text()')

        if len(response)==0:
            response = tree.xpath('//div[@class="tk_not_answered"]/text()')
            if len(response)==0:
                response = tree.xpath('//h3[@class="tk_text"]/text()')
                if len(response)==0:
                    raise Exception("irregular Response can't be parsed")
                else:
                    response = response[0].strip()
            else:
                response = response[0].strip()
        else:
            response = response[0].strip()
        if response == "Sorry, I don't yet have an answer to that question." or response=="":
            raise Exception("answer can't be answered by QA")
        return response

    def intro(self,text,context):
        return "You can ask me question like \"Why is sky blue ?\" or \"Who is Trump ?\""
