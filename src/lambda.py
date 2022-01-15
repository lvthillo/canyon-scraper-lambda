""" Scrape Canyon site."""
import requests
import os

import boto3
from bs4 import BeautifulSoup

client = boto3.client("sns")

url = "https://www.canyon.com/nl-be/road-bikes/endurance-bikes/endurace/cf-sl/endurace-cf-sl-8-disc/2948.html"
# url = "https://www.canyon.com/nl-be/gravel-bikes/bike-packing/grizl/cf-sl/grizl-cf-sl-8-suspension-1by/3237.html"


def lambda_handler(event, context):
    """Main."""
    page = requests.get(url)
    results = BeautifulSoup(page.content, "html.parser")

    items = []
    for div in results.findAll(
        "div", attrs={"class": "productConfiguration__availabilityMessage"}
    ):
        text = div.text
        items.append(text.strip())

    # size small is 3th of the list
    small_item = items[2]
    print("item: " + small_item)

    if small_item != "Uitverkocht":
        print("alert!")
        client.publish(
            TopicArn=os.environ["TOPIC"],
            Message="Time to buy a Canyon!",
            Subject="Time to buy a Canyon!",
        )
