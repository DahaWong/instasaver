'''
To generate a Telegraph-based preview of an Instapaper bookmark.
'''


from telegraph.aio import Telegraph
from telegraph.utils import ALLOWED_TAGS
from bs4 import BeautifulSoup
from constants import BOT_URL, BOT_NAME


def format_html(text):
    '''Format html texts that fetched from Instapaper to Telegraph allowed forms.'''
    soup = BeautifulSoup(text, 'lxml')

    # Find all possible heading types, and convert them to proper h3,h4,strong tags.
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    heading_types = sorted(set([x.name for x in headings]))
    if headings:
        for heading in headings:
            if heading.name == heading_types[0]:
                heading.name = 'h3'
            elif len(headings) >= 2 and heading.name == heading_types[1]:
                heading.name = 'h4'
            else:
                heading.name = 'strong'

    # a) Unwrap all unallowed tags and b) Remove all empty tags.
    ALLOWED_VOID_TAGS = {'br', 'img', 'figure',
                         'aside', 'iframe', 'ol', 'ul', 'hr'}
    for tag in soup.find_all():
        if tag.name not in ALLOWED_TAGS or (
           tag.name not in ALLOWED_VOID_TAGS and len(tag.get_text()) == 0
           ):
            tag.unwrap()
    print(soup.prettify())
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


# def main():
#     html = """<li>::before</li>"""
#     format_html(html)


# if __name__ == '__main__':
#     main()
