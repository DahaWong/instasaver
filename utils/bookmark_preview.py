from telegraph.aio import Telegraph
from telegraph.utils import ALLOWED_TAGS
from bs4 import BeautifulSoup


def format_html(text):
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
    telegraph = Telegraph()
    await telegraph.create_account(short_name='Instasaver')
    try:
        response = await telegraph.create_page(
            title=title,
            html_content=format_html(content),
            author_name='Instasaver',
            author_url='https://t.me/saveinstapaper_bot'
        )
        return response['url']
    except:
        return None
