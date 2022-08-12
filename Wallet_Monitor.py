import requests
from time import sleep

api_url = "https://api.helius.xyz/v0/addresses"
resource = "nft-events"
options_sale = 'api-key=4f87c21f-e412-4d7d-9cb9-28424c83508b&type=NFT_SALE'
options_listing = 'api-key=4f87c21f-e412-4d7d-9cb9-28424c83508b&type=NFT_LISTING'

cozy = "EAHJNfFDtivTMzKMNXzwAF9RTAeTd4aEYVwLjCiQWY1E"
sbb = "zbFjDhkc7RywwoywSgSSdTge7hwu68pgq5mXjY9WxRG"
hge = "DKddE8exaGxn3irDbUaadSSxY7W3jMCH9k3TRogoGM6v"
ravers = "AUrfsS5NudqC9Qt26mSJk7uGoi4xAcBNMbQUMt9PLy8G"
jagoe = "6zGfYoErdepGvGS1geu1sZUD3Gwms2CcjVS3Xu8aBfH5"

most_recent = "" 

first_latest_list = ""
first_prev_list = ""
first_temp_list = ""
first_latest_sale = ""
first_prev_sale = ""
first_temp_sale = ""

second_latest_list = ""
second_prev_list = ""
second_temp_list = ""
second_latest_sale = ""
second_prev_sale = ""
second_temp_sale = ""

third_latest_list = ""
third_prev_list = ""
third_temp_list = ""
third_latest_sale = ""
third_prev_sale = ""
third_temp_sale = ""

fourth_latest_list = ""
fourth_prev_list = ""
fourth_temp_list = ""
fourth_latest_sale = ""
fourth_prev_sale = ""
fourth_temp_sale = ""

fifth_latest_list = ""
fifth_prev_list = ""
fifth_temp_list = ""
fifth_latest_sale = ""
fifth_prev_sale = ""
fifth_temp_sale = ""

def initialize():
    first_sale = requests.get(f"{api_url}/{cozy}/{resource}?{options_sale}&until={most_recent}")
    sleep(2)
    first_list = requests.get(f"{api_url}/{cozy}/{resource}?{options_listing}&until={most_recent}")
    sleep(2)
    second_sale = requests.get(f"{api_url}/{sbb}/{resource}?{options_sale}&until={most_recent}")
    sleep(2)
    second_list = requests.get(f"{api_url}/{sbb}/{resource}?{options_listing}&until={most_recent}")
    sleep(2)
    third_sale = requests.get(f"{api_url}/{hge}/{resource}?{options_sale}&until={most_recent}")
    sleep(2)
    third_list = requests.get(f"{api_url}/{hge}/{resource}?{options_listing}&until={most_recent}")
    sleep(2)
    fourth_sale = requests.get(f"{api_url}/{ravers}/{resource}?{options_sale}&until={most_recent}")
    sleep(2)
    fourth_list = requests.get(f"{api_url}/{ravers}/{resource}?{options_listing}&until={most_recent}")
    sleep(2)
    fifth_sale = requests.get(f"{api_url}/{jagoe}/{resource}?{options_sale}&until={most_recent}")
    sleep(2)
    fifth_list = requests.get(f"{api_url}/{jagoe}/{resource}?{options_listing}&until={most_recent}")

    first_latest_sale = first_sale.json()
    first_latest_list = first_list.json()
    second_latest_sale = second_sale.json()
    second_latest_list = second_list.json()
    third_latest_sale = third_sale.json()
    third_latest_list = third_list.json()
    fourth_latest_sale = fourth_sale.json()
    fourth_latest_list = fourth_list.json()
    fifth_latest_sale = fifth_sale.json()
    fifth_latest_list = fifth_list.json()

