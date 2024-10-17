# TweetCounter
Uses the Twitter REST API to find and parse data using the provided query and outputs to an Excel Spreadsheet.

This relies on both the "TwitterAPI" and "xlsxwriter" packages. To install the dependencies, run:
```
pip install -r requirements.txt
```

# Setting Environment Variables

Before running the script, you need to set the following environment variables with your Twitter API credentials:
```
export API_KEY='your_api_key'
export API_SECRET='your_api_secret'
export ACCESS_TOKEN='your_access_token'
export ACCESS_TOKEN_SECRET='your_access_token_secret'
```

# Why?

My requirement was to count usages of a hashtag to compose a case study on a campaign and this was what I came up with to get some data together - hopefully someone else can find it useful.

Currently outputs 8 pieces of data, being the tweet count, username, tweet text, retweeted (true/false), retweet count, created at (time of tweet), favourited (true/false) and image url of media attached. 

If you require any further information please check example responses at: https://dev.twitter.com/rest/reference/get/search/tweets

It is not perfect and was just a small weekend project to allow me to get the information I needed.
