import tweepy
from dotenv import load_dotenv
import os

def GetTwitterAPI(api_key, api_secret, access_token, access_secret):

    auth = tweepy.OAuth1UserHandler(api_key, api_secret)
    auth.set_access_token(
        access_token,
        access_secret,
    )
    return tweepy.API(auth)


def GetTwitterClient(api_key, api_secret, access_token, access_secret):
    """Get twitter conn 2.0"""

    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret,
    )

    return client

def Tweet(TwitterPost, ImagePaths):

    load_dotenv("./.gitignore/.env")

    # get keys from .env
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_secret = os.getenv("ACCESS_SECRET")

    API = GetTwitterAPI(api_key, api_secret, access_token, access_secret)
    CLIENT = GetTwitterClient(api_key, api_secret, access_token, access_secret)

    media_ids = []
    for filename in ImagePaths:
        res = API.media_upload(filename)
        media_ids.append(res.media_id)

    # Post the image with a tweet
    try:
        CLIENT.create_tweet(text=TwitterPost, media_ids=media_ids)
        print("Tweet posted successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")


def main(TwitterPost, ImagePaths):
    Tweet(TwitterPost, ImagePaths)


if __name__ == '__main__':
    main()
