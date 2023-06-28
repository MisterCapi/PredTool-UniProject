import requests
import urllib.parse
from bs4 import BeautifulSoup

from structures.stat_classes import OverallPlayerStats, HeroPlayerStats


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
    mmr_value = 0
    soup = BeautifulSoup(player_stats.content, 'html.parser')
    mmr_span = soup.find('span', {'class': 'profile-mmr'})
    if mmr_span:
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
        if div_text[0] == "Matches":
            total_games = div_text[-1]
        elif div_text[1] == "KDA" and div_text[2] == "Ratio:":
            average_KDA_ratio = div_text[-1]
        elif div_text[1] == "KDA:":
            average_KDA = ' '.join(div_text[2:])
        elif div_text[1] == 'role:':
            favourite_role = div_text[-1]
        elif div_text[0] == 'Winrate:':
            win_rate = div_text[-1]

    # Extract hero stats
    hero_stats = soup.select('table.table-player-hero-stats > tbody > tr')
    hero_wr = '0%'
    hero_games = 0
    for tr in hero_stats:
        tr_text = tr.text.split()
        if len(tr_text) > 3:
            tr_text[0] = ' '.join(tr_text[:len(tr_text)-2])
        if hero_name == tr_text[0]:
            hero_wr = tr_text[-2]
            hero_games = tr_text[-1]
            break

    return {'overall_stats': OverallPlayerStats(mmr_rating=mmr_value,
                                                total_games=total_games,
                                                average_kda=average_KDA,
                                                kda_ratio=average_KDA_ratio,
                                                favourite_role=favourite_role,
                                                win_rate=win_rate),
            'hero_stats': HeroPlayerStats(total_games=hero_games,
                                          win_rate=hero_wr)}


if __name__ == '__main__':
    print(get_player_statistics("MrCapi", 'The Fey'))
