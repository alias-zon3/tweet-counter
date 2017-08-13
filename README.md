# TweetCounter
Uses the Twitter REST API to find and parse data using the provided query and outputs to an Excel Spreadsheet.

This relies on both the "TwitterAPI" and "xlsxwriter" packages, make sure to "pip install" both of these before executing the script and uninstall.

# Why?

My requirement was to count usages of a hashtag to compose a case study on a campaign and this was what I came up with to get some data together - hopefully someone else can find it useful.

Currently outputs 7 pieces of data, being the tweet count, username, tweet text, retweeted (true/false), retweet count, created at (time of tweet), favourited (true/false) and image url of media attached. 

If you require any further information please check example responses at: https://dev.twitter.com/rest/reference/get/search/tweets

It is not perfect and was just a small weekend project to allow me to get the information I needed.
