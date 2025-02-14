#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author         : yanyongyu
@Date           : 2021-03-26 14:59:59
@LastEditors    : yanyongyu
@LastEditTime   : 2022-10-04 10:08:41
@Description    : None
@GitHub         : https://github.com/yanyongyu
"""
__author__ = "yanyongyu"

from typing import ContextManager

from nonebot import on_command
from nonebot.log import logger
from githubkit.rest import Issue
from nonebot.adapters import Event
from nonebot.params import Depends
from nonebot.typing import T_State
from playwright.async_api import Error
from nonebot.adapters.github import GitHubBot, ActionTimeout
from nonebot.adapters.onebot.v11 import MessageSegment as QQMS

from src.plugins.github import config
from src.plugins.github.helpers import get_platform
from src.plugins.github.libs.renderer import pr_diff_to_html
from src.plugins.github.libs.message_tag import Tag, create_message_tag

from . import KEY_GITHUB_REPLY, is_github_reply
from .dependencies import get_issue, get_context

diff = on_command("content", is_github_reply, priority=config.github_command_priority)


@diff.handle()
async def handle_diff(
    event: Event,
    state: T_State,
    issue_: Issue = Depends(get_issue),
    context: ContextManager[GitHubBot] = Depends(get_context),
):
    tag: Tag = state[KEY_GITHUB_REPLY]

    try:
        with context:
            img = await pr_diff_to_html(issue_)
    except ActionTimeout:
        await diff.finish("GitHub API 超时，请稍后再试")
    except Error:
        await diff.finish("生成图片出错！请稍后再试")
    except Exception as e:
        logger.opt(exception=e).error(f"Failed while generating issue image: {e}")
        await diff.finish("生成图片出错！请稍后再试")

    match get_platform(event):
        case "qq":
            result = await diff.send(QQMS.image(img))
            if isinstance(result, dict) and "message_id" in result:
                await create_message_tag(
                    {"type": "qq", "message_id": result["message_id"]}, tag
                )
        case _:
            logger.error(f"Unprocessed event type: {type(event)}")
