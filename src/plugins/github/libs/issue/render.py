#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author         : yanyongyu
@Date           : 2021-05-14 17:09:12
@LastEditors    : yanyongyu
@LastEditTime   : 2021-05-21 15:04:44
@Description    : None
@GitHub         : https://github.com/yanyongyu
"""
__author__ = "yanyongyu"

from typing import Any
from pathlib import Path
from inspect import isclass
from datetime import datetime

import jinja2
import humanize
from unidiff import PatchSet
from nonebot.log import logger

from src.libs.github.models import Issue, TimelineEvent

env = jinja2.Environment(extensions=["jinja2.ext.loopcontrols"],
                         loader=jinja2.FileSystemLoader(
                             Path(__file__).parent / "templates"),
                         enable_async=True)


def classname(value: Any) -> str:
    return value.__name__ if isclass(value) else type(value).__name__


def relative_time(value: datetime):
    return humanize.naturaltime(datetime.now(value.tzinfo) - value)


def review_state(value: str) -> str:
    states = {
        "approved": "approved these changes",
        "changes_requested": "requested changes",
        "commented": "reviewed"
    }
    return states.get(value, value)


def debug_event(event: TimelineEvent):
    # not sub class of TimelineEvent
    if type(event) is TimelineEvent:
        # event not passed process
        logger.error(f"Unhandled event type: {event.event}", event=event.dict())
        return ""
    return event


env.filters["classname"] = classname
env.filters["relative_time"] = relative_time
env.filters["review_state"] = review_state
env.filters["debug_event"] = debug_event


async def issue_to_html(owner: str, repo_name: str, issue: Issue) -> str:
    template = env.get_template("issue.html")
    timeline = await issue.get_timeline()
    return await template.render_async(owner=owner,
                                       repo_name=repo_name,
                                       issue=issue,
                                       timeline=timeline)


async def pr_diff_to_html(owner: str, repo_name: str, issue: Issue) -> str:
    template = env.get_template("diff.html")
    diff = await issue.get_diff()
    return await template.render_async(owner=owner,
                                       repo_name=repo_name,
                                       issue=issue,
                                       diff=PatchSet(diff))
