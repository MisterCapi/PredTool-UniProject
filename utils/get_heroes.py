import os

import requests
from PIL import Image
from bs4 import BeautifulSoup


def download_hero_avatars():
    dashboard = requests.get("https://omeda.city/dashboard")

    hero_avatar_dir = 'hero_avatars'
    soup = BeautifulSoup(dashboard.content, 'html.parser')
    hero_divs = soup.select('div.hero-stats-hero')
    for div in hero_divs:
        hero_name = div.get_text(strip=True)
        img = div.select_one('img')
        hero_avatar_url = "https://omeda.city" + img.get('src')
        response = requests.get(hero_avatar_url)

        # Check that the request was successful
        os.makedirs(hero_avatar_dir, exist_ok=True)
        if response.status_code == 200:
            # Open a new file for writing in binary mode
            filename = f"{hero_name}.webp"
            filepath = os.path.join(hero_avatar_dir, filename)
            with open(filepath, 'wb') as file:
                # Write the contents of the response to the file
                file.write(response.content)
                print(f"Avatar for {hero_name} saved successfully!")

    for filename in os.listdir(hero_avatar_dir):
        if filename.endswith('.webp'):
            # Open the input image
            input_path = os.path.join(hero_avatar_dir, filename)
            with Image.open(input_path) as im:
                # Convert to PNG and save the output image
                output_path = os.path.join(hero_avatar_dir, os.path.splitext(filename)[0] + '.png')
                im.save(output_path, 'PNG')

            print(f"Image saved as {output_path}")
            # Remove the input file
            os.remove(input_path)
            print(f"Removed {input_path}")


if __name__ == '__main__':
    download_hero_avatars()
