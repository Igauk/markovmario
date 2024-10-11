import pickle
import re

import cv2
import numpy as np
import requests
from bs4 import BeautifulSoup


def scrape_map_images(title, short):
    """
    Fetches all images from the NES maps website for a certain game
    """
    base_url = "https://nesmaps.com/maps"

    page = requests.get(f"{base_url}/{title}/{title}BG.html")
    soup = BeautifulSoup(page.content, "html.parser")

    # Find all HTML links to map levels (each link appears twice, once as a link once as a thumbnail, keep just text)
    links = [link for link in soup.find_all(href=re.compile(f"{short}.*.html")) if link.next.name != 'img']

    images = []
    for link in links:
        # Each link leads to a page with a map image
        image_page = link['href']
        page = requests.get(f"{base_url}/{title}/{image_page}")
        soup = BeautifulSoup(page.content, "html.parser")

        image_src = soup.img['src']
        response = requests.get(f"{base_url}/{title}/{image_src}")
        image_array = np.frombuffer(response.content, np.uint8)
        images.append((image_src, cv2.cvtColor(cv2.imdecode(image_array, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)))
    return images


if __name__ == '__main__':
    SMB1_title = "SuperMarioBrothers"
    SMB1_short = "SuperMarioBros"
    SMB2_title = "SuperMarioBrothers2j"
    SMB2_short = "SuperMarioBros2j"

    SMB1_images = scrape_map_images(SMB1_title, SMB1_short)
    SMB2_images = scrape_map_images(SMB2_title, SMB2_short)

    with open("Scraped/smb1.pkl", 'wb') as f:
        pickle.dump(SMB1_images, f)

    with open("Scraped/smb2.pkl", 'wb') as f:
        pickle.dump(SMB2_images, f)
