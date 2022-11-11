# This file will look up all the people you follow on Twitter, and export them to a CSV file. It will also convert Twitter shortURLs into their real URLs.
# 
# No support or explanation provided. Feel free to use as-is.
# 
# Needs these to work, and you need to create an App under the Twitter API development platform (https://developer.twitter.com/en/portal/projects-and-apps) to get a bearer ID to request the data.
# 
# pip install tweepy
# pip install requests
# 
# Note, the code is not designed to be pretty or efficient. This was just a quick thing I needed.
# 
# -------------------------------------------


username = input('Username: ')
bearer = input('Twitter API bearer id (create an app under the Twitter API): ')

# pip install tweepy
# pip install requests

import tweepy
import requests
from concurrent.futures import ThreadPoolExecutor

# process all following
def processfollow(name,id,username,description,location,url,created_at,profile_image_url):
	shorturl,longurl = resolve_url(url)
	print(shorturl,'-->',longurl)
	following.append([name,id,username,description,location,longurl,created_at,profile_image_url])

# convert Twitter shorturl to the real URL
def resolve_url(url):
    try:
        r = requests.get(url,timeout=3)
    except requests.exceptions.RequestException:
        return (url, None)

    if r.status_code != 200:
        longurl = None
    else:
        longurl = r.url

    return (url, longurl)

following = []

client = tweepy.Client(bearer)

response = client.get_user(username=username)
userid = response.data.id

paginator = tweepy.Paginator(client.get_users_following, id=userid, expansions=['pinned_tweet_id'], user_fields=['profile_image_url','description','id', 'name', 'username', 'location', 'url',
		 'created_at', 'verified'], max_results=1000)

with ThreadPoolExecutor() as executor:
	for users in paginator:
		for user in users.data:
			print(user, user.id, user.description, user.profile_image_url)
			# processfollow(user.name,user.id,user.username,user.location,user.url,user.created_at,user.verified,user.profile_image_url)
			executor.submit(processfollow,user.name,user.id,user.username,user.description,user.location,user.url,user.created_at,user.profile_image_url)

with open(f'twitter-follow-{username}.csv', 'w', encoding='utf8') as fp:
	for user in following:
		userout = '","'.join(map(str, user))
		print(userout)
		fp.write(f'"{userout}"\n')
