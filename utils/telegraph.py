from telegraph.aio import Telegraph


async def create_page():
    telegraph = Telegraph()
    await telegraph.create_account(short_name='Instasaver')
    response = await telegraph.create_page(
        'Hey',
        html_content='<p>Hello, world!</p>',
    )
    print(response['url'])
