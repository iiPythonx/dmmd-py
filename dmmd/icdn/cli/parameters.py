# Copyright (c) 2025 iiPython

import asyncclick
from typing import Callable

# Actual parameter lists
search_params = [
    ("--begin",     int,                                                                         False, None,   "All content must have an associated time after the specified timestamp."),
    ("--end",       int,                                                                         False, None,   "All content must have an associated time before the specified timestamp."),
    ("--minimum",   int,                                                                         False, None,   "Content must have have a size in bytes greater then or equal to this."),
    ("--maximum",   int,                                                                         False, None,   "Content must have have a size in bytes less then or equal to this."),
    ("--count",     int,                                                                         True,  None,   "The number of UUIDs returned per page."),
    ("--loose",     bool,                                                                        False, False,  "If true, only require one filter to be true instead of all."),
    ("--order",     asyncclick.Choice(["asc", "dsc"], case_sensitive = False),                   False, "dsc",  "Sort UUIDs by ascending or descending order."),
    ("--page",      int,                                                                         False, None,   "Page offset."),
    ("--sort",      asyncclick.Choice(["name", "time", "uuid", "size"], case_sensitive = False), False, "time", "Sorting algorithm to use."),
    ("--tags",      str,                                                                         False, None,   "All content must contain the specified tags, seperated by a comma."),
    ("--uuid",      str,                                                                         False, None,   "Filter by an exact UUID."),
    ("--mime",      str,                                                                         False, None,   "Filter by an exact mimetype."),
    ("--extension", str,                                                                         False, None,   "Filter by an exact extension, excluding the dot."),
    ("--query",     bool,                                                                        True,  False,  "Show entire summaries instead of just UUIDs.")
]

generic_add = [
    ("--token", str, False, None, "Token to use for uploading."),
    ("--time",  int, False, None, "Millisecond based timestamp to use instead of the current time."),
]

# Handle attachment phase
def attach(params: list[tuple], function: Callable):
    for argument, type, is_flag, default, help in params:
        asyncclick.option(argument, type = type, is_flag = is_flag, default = default, help = help)(function)
