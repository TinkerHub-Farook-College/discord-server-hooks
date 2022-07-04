from requests import get, post
from random import randint, choice
from os import environ


def generate_embed(
        title,
        description,
        url,
        color,
        author_name,
        author_avatar,
        image_url,
        footer,
        fields=[]
):
    '''returns a discord compatible embed message with given attributes
    '''
    return {
        'embeds': [
            {
                'title': title,
                'description': description,
                'url': url,
                'color': color,
                'author': {
                    'name': author_name,
                    'icon_url': author_avatar
                },
                'image': {
                    'url': image_url
                },
                'fields': fields,
                'footer': {'text': footer}
            }
        ]
    }


def try_to_send(method, description: str):
    '''try to send the message by calling given `method`'''
    print('Sending', description, end=' ')
    try:
        method()
        print('✅')
    except:
        print('❌')


def random_meme():
    '''send a random meme from avaialable 1478 memes'''
    MEME_COUNT = 1478
    WEBHOOK_URL = environ['WEBHOOK_MEME']
    meme_id = randint(1, MEME_COUNT)
    meme_file = open(f'memes/{meme_id}.png', 'rb')
    meme = meme_file.read()
    meme_file.close()
    post(WEBHOOK_URL, files={'file': (
        f'Meme {meme_id}.png', meme, 'multipart/form-data')})


def random_quote():
    '''send a random quote from zenquotes.io'''
    WEBHOOK_URL = environ['WEBHOOK_QUOTE']
    quote = choice(get(
        'https://zenquotes.io/api/random').json())
    post(WEBHOOK_URL, {
         'content': f'\n\n >>> **Quote Of The Day**\n\n{quote["q"]}\n\n💠 __{quote["a"]}__ 💠\n'})


def random_article():
    '''send a random dev.to article'''
    WEBHOOK_URL = environ['WEBHOOK_NEWS']
    article = choice(get(
        'https://dev.to/api/articles', params={'top': 1}).json())
    article = generate_embed(article['title'], article['description'], article['url'], 0x5568FA,
                             article['user']['name'], article['user']['profile_image'], article['social_image'], f'❤️ {article["public_reactions_count"]} reactions . Published on {article["readable_publish_date"]}', [{'name': 'Tags', 'value': article['tags'], 'inline': False}])
    post(WEBHOOK_URL, article)


def main():
    try_to_send(random_article, 'random article')
    try_to_send(random_meme, 'random meme')
    try_to_send(random_quote, 'random quote')


if __name__ == '__main__':
    main()
