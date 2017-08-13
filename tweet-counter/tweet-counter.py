# Import the required libraries, make sure to "pip install" both "TwitterAPI" and "xlsxwriter". Don't forget to uninstall afterwards if you do not want to keep these libraries locally!
from TwitterAPI import TwitterAPI
from TwitterAPI import TwitterRestPager
import xlsxwriter

# Instantiate our api object using our api key, api secret, generated access token and access token secrets respectively
api = TwitterAPI('API_KEY', 'API_SECRET', 'ACCESS_TOKEN', 'ACCESS_TOKEN_SECRET')

# Create the workbook and add a worksheet to write to
workbook = xlsxwriter.Workbook('TweetCounter_Output.xlsx')
worksheet = workbook.add_worksheet()

# Create our headings
worksheet.write(0,0,'Tweet Count')
worksheet.write(0,1,'Username')
worksheet.write(0,2,'Tweet')
worksheet.write(0,3,'Retweeted')
worksheet.write(0,4,'Retweet Count')
worksheet.write(0,5,'Created At')
worksheet.write(0,6,'Favourited')
worksheet.write(0,7,'Image URL')

# Set up initial count and default data
count = 0
user = 'No user'
imageUrl = 'No image'
text = 'No text'
retweeted = 'false'
retweetCount = 0
createdAt = 'No time'
favorited = 'false'

# Return tweets, 100 at a time, with our chosen query (for hashtags, use "%23" to encode the hashtag character)
r = TwitterRestPager(api, 'search/tweets', {'q':'%23SomeHashtag', 'count':100})

# Loop through each item in the response, waiting 6 seconds between each request (as this should avoid our hourly limit)
for item in r.get_iterator(wait=6):
    # If we have text within this item then the tweet is valid
    if 'text' in item:
        # Update our variables
        count += 1
        text = item['text']
        retweeted = item['retweeted']
        retweetCount = item['retweet_count']
        createdAt = item['created_at']
        favorited = item['favorited']
        entities = item['entities']
        userObject = item['user']
        user = userObject['screen_name']
        
        # Check if we have any media, loop through each and set variable. Logic could use a sanity check as not sure how it works with multiple media urls?
        if 'media' in entities:
            for media in entities['media']:
                if 'media_url' in media:
                    imageUrl = media['media_url']
                else:
                    imageUrl = 'No image'
                    
    # We have hit a request limit, print error to console
    elif 'message' in item and item['code'] == 88:
        print('Request limit exceeded: %s' % item['message'])
        break

    # Write our data to the worksheet
    worksheet.write(count,0,count)
    worksheet.write(count,1,user)
    worksheet.write(count,2,text)
    worksheet.write(count,3,retweeted)
    worksheet.write(count,4,retweetCount)
    worksheet.write(count,5,createdAt)
    worksheet.write(count,6,favorited)
    worksheet.write(count,7,imageUrl)

# We have finished looping through our tweets, close and save this workbook. This saves to the same directory as the script by default.
workbook.close()
