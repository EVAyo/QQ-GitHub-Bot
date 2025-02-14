#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author         : yanyongyu
@Date           : 2022-09-02 11:35:48
@LastEditors    : yanyongyu
@LastEditTime   : 2022-09-02 12:10:42
@Description    : None
@GitHub         : https://github.com/yanyongyu
"""
__author__ = "yanyongyu"

from nonebot.rule import to_me
from nonebot import on_type, on_message
from nonebot.adapters.onebot.v11 import PokeNotifyEvent, PrivateMessageEvent

from . import server_status, status_permission

group_poke = on_type(
    (PokeNotifyEvent,),
    rule=to_me(),
    permission=status_permission,
    priority=10,
    block=True,
    handlers=[server_status],
)


async def _poke(event: PrivateMessageEvent) -> bool:
    return event.sub_type == "friend" and event.message[0].type == "poke"


poke = on_message(
    _poke,
    permission=status_permission,
    priority=10,
    block=True,
    handlers=[server_status],
)
