""" Scrape Canyon site."""
import requests
import os

import boto3
from bs4 import BeautifulSoup

client = boto3.client("sns")
url = "https://www.canyon.com/nl-be/road-bikes/endurance-bikes/endurace/cf-sl/endurace-cf-sl-8/3364.html?dwvar_3364_pv_rahmenfarbe=GY%2FBK"
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

    # size small is 4th of the list
    small_item = items[3]
    print("item: " + small_item)

    if "Binnenkort" not in small_item:
        print("alert!")
        client.publish(
            TopicArn=os.environ["TOPIC"],
            Message="Time to buy a Canyon!",
            Subject="Time to buy a Canyon!",
        )
