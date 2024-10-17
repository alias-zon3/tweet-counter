import os
from TwitterAPI import TwitterAPI, TwitterRestPager
import xlsxwriter
from typing import Any, Dict

def get_twitter_api() -> TwitterAPI:
    api_key = os.getenv('API_KEY')
    api_secret = os.getenv('API_SECRET')
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
    return TwitterAPI(api_key, api_secret, access_token, access_token_secret)

def create_workbook(filename: str) -> xlsxwriter.Workbook:
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'Tweet Count')
    worksheet.write(0, 1, 'Username')
    worksheet.write(0, 2, 'Tweet')
    worksheet.write(0, 3, 'Retweeted')
    worksheet.write(0, 4, 'Retweet Count')
    worksheet.write(0, 5, 'Created At')
    worksheet.write(0, 6, 'Favourited')
    worksheet.write(0, 7, 'Image URL')
    return workbook

def fetch_tweets(api: TwitterAPI, query: str) -> Any:
    return TwitterRestPager(api, 'search/tweets', {'q': query, 'count': 100})

def process_tweet(item: Dict[str, Any]) -> Dict[str, Any]:
    tweet_data = {
        'count': 0,
        'user': 'No user',
        'imageUrl': 'No image',
        'text': 'No text',
        'retweeted': 'false',
        'retweetCount': 0,
        'createdAt': 'No time',
        'favorited': 'false'
    }
    if 'text' in item:
        tweet_data['text'] = item['text']
        tweet_data['retweeted'] = item['retweeted']
        tweet_data['retweetCount'] = item['retweet_count']
        tweet_data['createdAt'] = item['created_at']
        tweet_data['favorited'] = item['favorited']
        tweet_data['user'] = item['user']['screen_name']
        if 'media' in item['entities']:
            for media in item['entities']['media']:
                if 'media_url' in media:
                    tweet_data['imageUrl'] = media['media_url']
    return tweet_data

def main():
    api = get_twitter_api()
    workbook = create_workbook('TweetCounter_Output.xlsx')
    worksheet = workbook.get_worksheet_by_name('Sheet1')
    count = 0

    try:
        tweets = fetch_tweets(api, '%23SomeHashtag')
        for item in tweets.get_iterator(wait=6):
            if 'message' in item and item['code'] == 88:
                print(f'Request limit exceeded: {item["message"]}')
                break
            tweet_data = process_tweet(item)
            count += 1
            worksheet.write(count, 0, count)
            worksheet.write(count, 1, tweet_data['user'])
            worksheet.write(count, 2, tweet_data['text'])
            worksheet.write(count, 3, tweet_data['retweeted'])
            worksheet.write(count, 4, tweet_data['retweetCount'])
            worksheet.write(count, 5, tweet_data['createdAt'])
            worksheet.write(count, 6, tweet_data['favorited'])
            worksheet.write(count, 7, tweet_data['imageUrl'])
    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        workbook.close()

if __name__ == '__main__':
    main()
