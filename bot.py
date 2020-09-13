# -*- coding: utf-8 -*-
"""Modules for vk bot"""
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from parse import get_data
import config

def main():
    """
    Main connect to vk_api
    Set vk group id and token in .env file
    """
    vk_session = vk_api.VkApi(token=config.VK_TOKEN)
    longpoll = VkBotLongPoll(vk_session, config.VK_GROUP_ID)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            peer_id = event.object.message['peer_id']
            nickname = event.object.message['text']
            stats = get_data(nickname)
            vk_session.method("messages.send", {"peer_id": peer_id, "random_id": get_random_id(), "message": stats})

if __name__ == "__main__":
    main()
