#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author         : yanyongyu
@Date           : 2021-03-25 15:20:47
@LastEditors    : yanyongyu
@LastEditTime   : 2022-10-21 03:40:20
@Description    : None
@GitHub         : https://github.com/yanyongyu
"""
__author__ = "yanyongyu"

from nonebot.params import Depends
from nonebot.typing import T_State
from nonebot.plugin import PluginMetadata
from nonebot.message import event_preprocessor

from src.plugins.github.libs.message_tag import MessageInfo, get_message_tag

KEY_GITHUB_REPLY = "github:reply"

from .dependencies import get_reply

__plugin_meta__ = PluginMetadata(
    "GitHub 消息快捷命令",
    "通过回复 GitHub 消息来快速进行 Issue、PR 相关操作",
    (
        "/link: 获取 Issue/PR 链接\n"
        "/repo: 获取仓库链接\n"
        "/star: star 仓库（仅仓库安装 APP 后有效）\n"
        "/unstar: unstar 仓库（仅仓库安装 APP 后有效）\n"
        "/content: 查看 Issue、PR 信息及事件\n"
        "/diff: 查看 PR diff"
    ),
)


@event_preprocessor
async def check_reply(state: T_State, info: MessageInfo = Depends(get_reply)):
    if tag := await get_message_tag(info):
        # inject reply info into state
        state[KEY_GITHUB_REPLY] = tag


from . import diff, link, repo, content
