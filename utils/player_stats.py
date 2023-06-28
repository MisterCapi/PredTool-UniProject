import requests
import urllib.parse
from bs4 import BeautifulSoup


def get_player_statistics(player_name: str, hero_name: str):
    username = ""
    for char in player_name:
        if char.isalnum() or char == ' ':
            username += char
        else:
            break
    possible_players = requests.get(f"https://omeda.city/search?sq={urllib.parse.quote_plus(username)}")
    soup = BeautifulSoup(possible_players.content, 'html.parser')
    search_results = soup.find_all('a', {'class': 'search-result'})
    hrefs = [result.get('href') for result in search_results]
    hrefs = ["https://omeda.city" + href for href in hrefs]
    if not hrefs:
        return 0, '0%', '0 / 0 / 0', '0', '0', '-', '0%', '0', '0'
    player_stats = requests.get(hrefs[0])

    # Extract mmr
    soup = BeautifulSoup(player_stats.content, 'html.parser')
    mmr_span = soup.find('span', {'class': 'profile-mmr'})
    mmr_text = mmr_span.text.strip()
    if any(c.isalpha() for c in mmr_text.split()[0]):
        mmr_value = 0
    else:
        mmr_value = float(mmr_text.split()[0])

    # Extract total games
    soup = BeautifulSoup(player_stats.content, 'html.parser')
    profile_divs = soup.find_all('div', {'class': 'profile-row'})
    total_games = 0
    average_KDA = '0 / 0 / 0'
    average_KDA_ratio = 0
    win_rate = '0%'
    favourite_role = "None"
    for div in profile_divs:
        div_text = div.text.split()
        if div_text[0] == "Total":
            total_games = div_text[-1]
        elif div_text[1] == "KDA" and div_text[2] == "Ratio:":
            average_KDA_ratio = div_text[-1]
        elif div_text[1] == "KDA:":
            average_KDA = ' '.join(div_text[2:])
        elif div_text[1] == 'role:':
            favourite_role = div_text[-1]
        elif div_text[0] == 'Win':
            win_rate = div_text[-1]

    # Extract hero stats
    hero_stats = soup.select('table.table-player-hero-stats > tbody > tr')
    hero_wr = '0%'
    hero_KDA = 0
    hero_games = 0
    for tr in hero_stats:
        tr_text = tr.text.split()
        if len(tr_text) > 4:
            tr_text[0] = ' '.join(tr_text[:len(tr_text)-3])
        if hero_name == tr_text[0]:
            hero_wr = tr_text[-3]
            hero_KDA = tr_text[-2]
            hero_games = tr_text[-1]
            break

    return (mmr_value, win_rate, average_KDA, average_KDA_ratio, total_games, favourite_role, hero_wr, hero_KDA, hero_games)


if __name__ == '__main__':
    print(get_player_statistics("AGoRA_FOREVER", 'The Fey'))
