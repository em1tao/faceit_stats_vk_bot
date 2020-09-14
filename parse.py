# -*- coding: utf-8 -*-
"""Modules for parsing"""
import json
import requests
import config

headers = {"accept": "application/json",
           "Authorization": f"Bearer {config.FACEIT_TOKEN}"}

def get_data(nickname):
    """
    nickname: nickname of the player
    """
    # First we get player's id, elo and level
    player_request = requests.get(f"https://open.faceit.com/data/v4/players?nickname={nickname}", headers=headers)
    if player_request.status_code == 200:
        player = json.loads(player_request.content)
        player_data = player["games"]["csgo"]
        # Then get K/D, HS%, WR%
        stats_request = requests.get(f"https://open.faceit.com/data/v4/players/{player['player_id']}/stats/csgo", headers=headers)
        stats = json.loads(stats_request.content)["lifetime"]
        # Making message to send using stats that were recieved
        stats_message = f"{nickname}\n&#9889;LVL - {player_data['skill_level']} &#9889;" \
                        f"\n&#128142;ELO - {player_data['faceit_elo']} &#128142;" \
                        f"\n&#128299;K/D - {stats['Average K/D Ratio']} &#128299;" \
                        f"\n&#128128;Headshots - {stats['Average Headshots %']} % &#128128;" \
                        f"\n&#128302;Winrate - {stats['Win Rate %']} % &#128302;"
        return stats_message
    if player_request.status_code == 404:
        return "Игрок не найден"
    return "Произошла ошибка"
