from lxml import html
import requests
domain = 'https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/speechcon-reference'
page = requests.get(domain)
tree = html.fromstring(page.content)
responce =  tree.xpath('//audio/@title')
print(responce)
