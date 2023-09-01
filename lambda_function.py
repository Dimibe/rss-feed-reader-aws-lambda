import boto3
import feedparser
import json
from dateutil import parser

def lambda_handler(e, context):
    """
    :type event: object
    :param event:
    :param context:
    :return:
    """
    with open('event.json') as json_file:
        event = json.loads(json_file.read())
    dynamodb = boto3.client('dynamodb')
    for object in event:
        table_name = object['table_name']
        for rss_url in object['rss_urls']:
            feed = feedparser.parse(rss_url)
            for item in feed['items']:
                print(item)
                try:
                    id = item['id']

                    if item.get('author'):
                        author = item.get('author')
                    else:
                        author = '-'

                    if item.get('link'):
                        link = item.get('link')
                    else:
                        link = '-'
                    
                    if item.get('title'):
                        title = item.get('title')
                    else:
                        title = '-'

                    if feed.get("version"):
                        channel_version = feed.get("version")
                    else:
                        channel_version = '-'

                    if feed.get("channel"):
                        channel_title = feed["channel"]["title"]
                        channel_description = feed["channel"]["description"]
                        channel_link = feed["channel"]["link"]
                    else:
                        channel_title = '-'
                        channel_description = '-'
                        channel_link = '-'
                    
                    if item.get('published'):
                        published = parser.parse(item['published']).isoformat()
                    else:
                        published = '-'
                    
                    if item.get('summary') != "":
                        summary = item['summary']
                    else:
                        summary = item['title']

                    if item.get('tags'):
                        term = item['tags'][0]['term']\
                            .replace("general:products/", "")\
                            .title()\
                            .split(",")[0]
                    else:
                        term = 'New'

                    response = dynamodb.put_item(
                        TableName=object['table_name'],
                        ConditionExpression='attribute_not_exists(id)',
                        Item={
                            'id': {
                                'S': id
                            },
                            'author': {
                                'S': author
                            },
                            'published': {
                                'S': published
                            },
                            'link': {
                                'S': link
                            },
                            'summary': {
                                'S': summary
                            },
                            'title': {
                                'S': title
                            },
                            'term': {
                                'S': term
                            },
                            'channel_version': {
                                'S': channel_version
                            },
                            'channel_title': {
                                'S': channel_title
                            },
                            'channel_description': {
                                'S': channel_description
                            },
                            'channel_link': {
                                'S': channel_link
                            }
                        }
                    )
                    print(response)
                except dynamodb.exceptions.ConditionalCheckFailedException as e:
                    pass
                except Exception as e:
                    print(e)
                
if __name__ == "__main__":
    lambda_handler('[]', '')
