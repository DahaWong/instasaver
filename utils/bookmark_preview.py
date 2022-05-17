'''
To genrate a Telegraph-based preview of a Instapaper bookmark.
'''


from telegraph.aio import Telegraph
from telegraph.utils import ALLOWED_TAGS
from bs4 import BeautifulSoup
from constants import BOT_URL, BOT_NAME


def format_html(text):
    '''Format html texts that fetched from Instapaper to Telegraph allowed forms.'''
    soup = BeautifulSoup(text, 'lxml')
    # Format headings, h1 -> h3, h2 -> h4, and other headings to <strong> tag.
    for h1 in soup.find_all('h1'):
        h1.name = 'h3'
    for h2 in soup.find_all('h2'):
        h2.name = 'h4'
    for other_heading in soup.find_all('h3', 'h4', 'h5', 'h6'):
        other_heading.name = 'strong'
    # Unwrap(i.e. remove) all unallowed tags.
    unallowed_tags = filter(
        lambda x: x.name not in ALLOWED_TAGS, soup.find_all())
    for tag in unallowed_tags:
        tag.unwrap()
    return str(soup)


async def create_page(title, content):
    '''Create a Telegraph account and generate page with title and content.'''
    telegraph = Telegraph()
    await telegraph.create_account(short_name=BOT_NAME)
    try:
        response = await telegraph.create_page(
            title=title,
            html_content=format_html(content),
            author_name=BOT_NAME,
            author_url=BOT_URL
        )
        return response['url']
    except:
        return None
