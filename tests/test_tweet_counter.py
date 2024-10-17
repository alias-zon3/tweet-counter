import os
import unittest
from unittest.mock import patch, MagicMock
from tweet_counter import get_twitter_api, create_workbook, fetch_tweets, process_tweet, main

class TestTweetCounter(unittest.TestCase):

    @patch('tweet_counter.TwitterAPI')
    def test_get_twitter_api(self, MockTwitterAPI):
        mock_api = MockTwitterAPI.return_value
        os.environ['API_KEY'] = 'test_api_key'
        os.environ['API_SECRET'] = 'test_api_secret'
        os.environ['ACCESS_TOKEN'] = 'test_access_token'
        os.environ['ACCESS_TOKEN_SECRET'] = 'test_access_token_secret'
        api = get_twitter_api()
        self.assertEqual(api, mock_api)

    def test_create_workbook(self):
        workbook = create_workbook('test.xlsx')
        self.assertIsNotNone(workbook)
        worksheet = workbook.get_worksheet_by_name('Sheet1')
        self.assertIsNotNone(worksheet)
        self.assertEqual(worksheet.name, 'Sheet1')
        workbook.close()

    @patch('tweet_counter.TwitterRestPager')
    def test_fetch_tweets(self, MockTwitterRestPager):
        mock_pager = MockTwitterRestPager.return_value
        api = MagicMock()
        query = 'test_query'
        tweets = fetch_tweets(api, query)
        self.assertEqual(tweets, mock_pager)

    def test_process_tweet(self):
        item = {
            'text': 'test tweet',
            'retweeted': False,
            'retweet_count': 10,
            'created_at': 'Wed Oct 10 20:19:24 +0000 2018',
            'favorited': False,
            'user': {'screen_name': 'test_user'},
            'entities': {'media': [{'media_url': 'http://test.com/image.jpg'}]}
        }
        tweet_data = process_tweet(item)
        self.assertEqual(tweet_data['text'], 'test tweet')
        self.assertEqual(tweet_data['retweeted'], False)
        self.assertEqual(tweet_data['retweetCount'], 10)
        self.assertEqual(tweet_data['createdAt'], 'Wed Oct 10 20:19:24 +0000 2018')
        self.assertEqual(tweet_data['favorited'], False)
        self.assertEqual(tweet_data['user'], 'test_user')
        self.assertEqual(tweet_data['imageUrl'], 'http://test.com/image.jpg')

    @patch('tweet_counter.get_twitter_api')
    @patch('tweet_counter.create_workbook')
    @patch('tweet_counter.fetch_tweets')
    @patch('tweet_counter.process_tweet')
    def test_main(self, mock_process_tweet, mock_fetch_tweets, mock_create_workbook, mock_get_twitter_api):
        mock_api = MagicMock()
        mock_get_twitter_api.return_value = mock_api
        mock_workbook = MagicMock()
        mock_create_workbook.return_value = mock_workbook
        mock_worksheet = MagicMock()
        mock_workbook.get_worksheet_by_name.return_value = mock_worksheet
        mock_tweet = {
            'text': 'test tweet',
            'retweeted': False,
            'retweet_count': 10,
            'created_at': 'Wed Oct 10 20:19:24 +0000 2018',
            'favorited': False,
            'user': {'screen_name': 'test_user'},
            'entities': {'media': [{'media_url': 'http://test.com/image.jpg'}]}
        }
        mock_fetch_tweets.return_value.get_iterator.return_value = [mock_tweet]
        mock_process_tweet.return_value = {
            'text': 'test tweet',
            'retweeted': False,
            'retweetCount': 10,
            'createdAt': 'Wed Oct 10 20:19:24 +0000 2018',
            'favorited': False,
            'user': 'test_user',
            'imageUrl': 'http://test.com/image.jpg'
        }

        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_not_called()
            mock_worksheet.write.assert_called()

if __name__ == '__main__':
    unittest.main()
