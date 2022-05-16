'''
API request methods for manipulating Instapaper account.

1.All request should be made by POST method.
'''

from config import oauth_consumer_id, oauth_consumer_secret
import urllib
import oauth2 as oauth
import json
import ast

root = 'https://www.instapaper.com/'
apis = {
    'access_token': 'api/1/oauth/access_token',
    'verify': 'api/1/account/verify_credentials',
    'save': 'api/1/bookmarks/add',
    'delete': 'api/1/bookmarks/delete',
    'like': 'api/1/bookmarks/star',
    'unlike': 'api/1/bookmarks/unstar',
    'archive': 'api/1/bookmarks/archive',
    'unarchive': 'api/1/bookmarks/unarchive',
    'list': 'api/1/bookmarks/list',
    'get_text': 'api/1/bookmarks/get_text',
}


def get_client(data):
    consumer = oauth.Consumer(oauth_consumer_id, oauth_consumer_secret)
    client = oauth.Client(consumer)
    client.add_credentials(data['username'], data['password'])
    client.authorizations

    params = {
        "x_auth_username": data['username'],
        "x_auth_password": data['password'],
        "x_auth_mode": 'client_auth'
    }

    client.set_signature_method = oauth.SignatureMethod_HMAC_SHA1()
    res, token = client.request(
        root + apis['access_token'],
        method="POST",
        body=urllib.parse.urlencode(params)
    )

    if not res['status'] == '200':
        return False
    else:
        access_token = dict(urllib.parse.parse_qsl(token))
        access_token = oauth.Token(
            access_token[b'oauth_token'], access_token[b'oauth_token_secret'])
        client = oauth.Client(consumer, access_token)
        return client


def verify_user(client):
    _, user_data = client.request(
        root + apis['verify'],
        method="POST"
    )
    user_data = json.loads(user_data)[0]
    return user_data


def list_all(client):
    params = {"limit": 100}
    bookmarks = client.request(
        root + apis['list'],
        method="POST",
        body=urllib.parse.urlencode(params)
    )[1].decode('utf-8')
    bookmarks = json.loads(bookmarks)
    return filter(lambda x: x['type'] == "bookmark", bookmarks)


def get_text(client, bookmark_id):
    """Get full text of a bookmark in html format."""
    params = {"bookmark_id": bookmark_id}
    html_text = client.request(
        root + apis['get_text'],
        method="POST",
        body=urllib.parse.urlencode(params)
    )[1].decode('utf-8')

    return html_text


def save(client, url):
    params = {"url": url}
    bookmark = ast.literal_eval(
        client.request(
            root + apis['save'],
            method="POST",
            body=urllib.parse.urlencode(params)
        )[1].decode('utf-8')
    )
    return (bookmark[0]['bookmark_id'], bookmark[0]['title'])


def delete(client, bookmark_id):
    params = {"bookmark_id": bookmark_id}
    empty = ast.literal_eval(client.request(
        root + apis['delete'],
        method="POST",
        body=urllib.parse.urlencode(params)
    )[1].decode('utf-8'))
    if (empty):
        return False
    else:
        return True


def like(client, bookmark_id):
    params = {"bookmark_id": bookmark_id}
    bookmark = ast.literal_eval(client.request(
        root + apis['like'],
        method="POST",
        body=urllib.parse.urlencode(params)
    )[1].decode('utf-8'))
    if (int(bookmark[0]['starred'])):
        return True
    else:
        return False


def unlike(client, bookmark_id):
    params = {"bookmark_id": bookmark_id}
    bookmark = ast.literal_eval(client.request(
        root + apis['unlike'],
        method="POST",
        body=urllib.parse.urlencode(params)
    )[1].decode('utf-8'))
    if (int(bookmark[0]['starred'])):
        return False
    else:
        return True
