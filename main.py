import os

from utils.get_heroes import download_hero_avatars
from utils.ocr_extractor import extract_usernames_and_heroes
from utils.player_stats import get_player_statistics
from utils.put_stats_on_image import put_stats_on_image
from utils.screenshot import get_game_screenshot

if not os.path.exists('hero_avatars'):
    download_hero_avatars()

# screenshot_path = get_game_screenshot()
screenshot_path = "screenshot.png"

usernames, heroes = extract_usernames_and_heroes(screenshot_path)
player_stats = []
for username, hero in zip(usernames, heroes):
    player_stats.append(get_player_statistics(username, hero))

put_stats_on_image(player_stats)

