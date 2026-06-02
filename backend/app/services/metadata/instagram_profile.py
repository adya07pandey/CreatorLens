from apify_client import ApifyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = ApifyClient(
    os.getenv("APIFY_TOKEN")
)


def get_follower_count(username):

    run_input = {
        "usernames": [username]
    }

    run = client.actor(
        "apify/instagram-followers-count-scraper"
    ).call(
        run_input=run_input
    )

    dataset = client.dataset(
        run["defaultDatasetId"]
    )

    items = list(
        dataset.iterate_items()
    )

    if not items:
        return 0

    item = items[0]

    return item.get(
        "followersCount",
        0
    )