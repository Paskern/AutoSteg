import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import hashlib
import time
import shutil
import tempfile

def get_image_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    img_tags = soup.find_all('img')
    img_links = [urljoin(url, img.get('src')) for img in img_tags]
    return img_links

def download_image(url, download_directory):
    response = requests.get(url, stream=True)
    file_name = url.split("/")[-1]
    temp_file_path = os.path.join(download_directory, next(tempfile._get_candidate_names()))

    with open(temp_file_path, 'wb') as file:
        shutil.copyfileobj(response.raw, file)
    
    return temp_file_path, file_name

def md5_file(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
    return hashlib.md5(content).hexdigest()

def main(url, download_directory, interval):
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)
    
    downloaded_images_hash = set()

    while True:
        try:
            image_links = get_image_links(url)
            for link in image_links:
                _, file_type = os.path.splitext(link)
                if file_type.lower() in ['.jpg', '.jpeg', '.bmp']:
                    temp_path, file_name = download_image(link, download_directory)
                    md5_hash = md5_file(temp_path)

                    if md5_hash not in downloaded_images_hash:
                        downloaded_images_hash.add(md5_hash)
                        final_path = os.path.join(download_directory, file_name)
                        os.rename(temp_path, final_path)
                        print(f"[+] Successfully downloaded {link}")
                    else:
                        os.remove(temp_path)
        except Exception as e:
            print(f"[!] Error while processing: {e}")
        
        print(f"[+] Sleeping for {interval} seconds")
        time.sleep(interval)

if __name__ == "__main__":
    url = "https://vg.no"
    download_directory = "downloaded_images"
    interval = 15 # Seconds

    main(url, download_directory, interval)