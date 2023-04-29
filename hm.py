import os
import pandas as pd
import requests
from bs4 import BeautifulSoup as BS

df = pd.read_excel(r"C:\Users\MyPc\Desktop\Others\Job\ZALORA\4. Required Files\Question 1 Dataset.xlsx")
article_numbers = df["Article Number"].tolist()

def scrape_images_and_videos(article_number):
    # Create folder for article number
    folder_path = str(article_number)
    os.makedirs(folder_path, exist_ok=True)

    # Send GET request to PDV page
    url = f"https://www2.hm.com/en_us/productpage.{article_number}.html"
    response = requests.get(url)

    # Parse HTML content with BS
    soup = BS(response.content, "html.parser")

    # Find all image URLs and download them
    img_tags = soup.find_all("img", {"class": "product-detail-main-image"})
    for i, img_tag in enumerate(img_tags):
        img_url = img_tag["src"]
        img_response = requests.get(img_url)
        img_path = f"{folder_path}/{i+1}.jpg"
        with open(img_path, "wb") as f:
            f.write(img_response.content)

    # Find all video URLs and download them
    video_tags = soup.find_all("video", {"class": "product-detail-main-video"})
    for i, video_tag in enumerate(video_tags):
        video_url = video_tag.find("source")["src"]
        video_response = requests.get(video_url)
        video_path = f"{folder_path}/{i+1}.mp4"
        with open(video_path, "wb") as f:
            f.write(video_response.content)
            
for article_number in article_numbers:
    scrape_images_and_videos(article_number)