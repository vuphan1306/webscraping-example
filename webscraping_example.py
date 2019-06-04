import os
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Specifying incognito mode as you launch your browser[OPTIONAL]
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
option.add_argument("headless")

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "bin/chromedriver")

# Create new Instance of Chrome in incognito mode
browser = webdriver.Chrome(executable_path=DRIVER_BIN, options=option)

AMAZON_URL = "https://www.amazon.com/Womens-Novelty-T-Shirts/b/ref=dp_bc_aui_C_7?ie=UTF8&node=9056923011"

# Go to desired website
browser.get(AMAZON_URL)

# Wait 20 seconds for page to load
timeout = 20
try:
    # Wait until the final element [Avatar link] is loaded.
    # Assumption: If Avatar link is loaded, the whole page would be relatively loaded because it is among
    # the last things to be loaded.
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//img[@class='s-access-image cfMarker']")))
except TimeoutException:
    browser.quit()

# find_elements_by_xpath - Returns an array of selenium objects.
# List Comprehension to get name and not the selenium objects.
product_names = browser.find_elements_by_xpath("""
    //div[@class='a-column a-span12 a-text-center']
    /a[@class='a-link-normal a-text-normal']
    /span[@class='a-color-secondary s-overflow-ellipsis s-size-mild']
""")
names = [x.text for x in product_names]

# product_descriptions = browser.find_elements_by_xpath("""
#     //div[@class='a-row a-spacing-micro']
#     /a[@class='a-link-normal s-access-detail-page s-overflow-ellipsis s-color-twister-title-link a-text-normal']
#     /h2[@class='a-size-small a-color-base s-inline s-access-title a-text-normal']
# """)
# descriptions = [x.text for x in product_descriptions]

# product_prices = browser.find_elements_by_xpath("//span[@class='sx-price-whole']")
# prices = [x.text for x in product_prices]

# product_images = browser.find_elements_by_xpath("//img[@class='s-access-image cfMarker']")
# images = [x.text for x in product_images]

def export_csv(data):
    """
    Export CSV file from data input
    """

    with open("amazon-data.csv", mode="w") as csv_file:
        fieldnames = ["PRODUCT NAME", "DESCRIPTION", "PRICE", "IMAGE URL"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for idx, name in enumerate(data.get("names", [])):
            writer.writerow(
                {
                    "PRODUCT NAME": name
                }
            )
            # writer.writerow(
            #     {
            #         "PRODUCT NAME": name,
            #         "DESCRIPTION": data.get("descriptions", [])[idx],
            #         "PRICE": data.get("prices", [])[idx],
            #         "IMAGE URL": data.get("images", [])[idx]
            #     }
            # )
    csv_file.close()

data = {}
data["names"] = names
# data["descriptions"] = descriptions
# data["prices"] = prices
# data["images"] = images

export_csv(data)
browser.quit()