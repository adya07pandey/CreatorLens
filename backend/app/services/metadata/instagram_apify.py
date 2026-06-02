from apify_client import ApifyClient
from dotenv import load_dotenv
import os

from app.utils.metadata import normalize_metadata

load_dotenv()

client = ApifyClient(os.getenv("APIFY_TOKEN"))


def get_reel_data(url):

    run_input = {
        "username": [url],
        "includeTranscript": True
    }

    run = client.actor("apify/instagram-reel-scraper").call(run_input=run_input)
    print(type(run))
    print(run)
    dataset = client.dataset(
        run.default_dataset_id
    )

    items = list(dataset.iterate_items())

    if not items:
        raise Exception("No reel data returned")

    return items[0]


def extract_apify_metadata(item):

    raw = {
        "title": item.get("caption"),
        "caption": item.get("caption"),
        "creator": item.get("ownerUsername"),
        "creator_name": item.get("ownerFullName"),
        "likes": item.get("likesCount"),
        "comments": item.get("commentsCount"),
        "shares": item.get("sharesCount"),
        "views": item.get("videoViewCount"),
        "hashtags": item.get("hashtags"),
        "duration": item.get("videoDuration"),
        "thumbnail": item.get("displayUrl"),
        "timestamp": item.get("timestamp"),
        "platform": "instagram",
    }
    print(raw)
    return normalize_metadata(raw)
