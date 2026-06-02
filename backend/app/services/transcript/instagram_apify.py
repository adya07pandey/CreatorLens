from apify_client import ApifyClient
from app.services.metadata.instagram_apify import get_reel_data
from dotenv import load_dotenv
import os

load_dotenv()

client = ApifyClient(
    os.getenv("APIFY_TOKEN")
)

def get_apify_transcript(url):

    item = get_reel_data(url)

    transcript = item.get(
        "transcript"
    )

    if not transcript:

        raise Exception(
            "Transcript missing"
        )

    return transcript