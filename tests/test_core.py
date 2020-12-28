# -*- coding: utf-8 -*-
# (c) 2020 Martin Wendt and contributors; see https://github.com/mar10/yabs
# Licensed under the MIT license: https://www.opensource.org/licenses/mit-license.php
"""
"""
from io import StringIO

from snazzy import (
    Snazzy,
    ansi,
    ansi_reset,
    colors_enabled,
    demo,
    emoji,
    enable_colors,
    gray,
    green,
    red,
    wrap,
    yellow,
)

# import pytest


class TestBasics:
    def test_basics(self):

        assert not colors_enabled()
        assert red("error") == "error"
        assert green("ok") == "ok"

        enable_colors(True, True)
        assert red("error") == "\x1b[91merror\x1b[39m"
        assert green("ok") == "\x1b[32mok\x1b[39m"
        assert yellow("warn") == "\x1b[93mwarn\x1b[39m"
        assert gray("debug") == "\x1b[90mdebug\x1b[39m"

        assert wrap("foo", bold=True) == "\x1b[1mfoo\x1b[22m"
        assert wrap("foo", italic=True) == "\x1b[3mfoo\x1b[23m"
        assert wrap("foo", underline=True) == "\x1b[4mfoo\x1b[24m"

        assert ansi(bold=True) == "\x1b[1m"
        assert ansi_reset() == "\x1b[0m"
        assert ansi_reset(fg=False) == "\x1b[49m\x1b[22m\x1b[23m\x1b[24m"

        assert wrap("foo", (80, 80, 80)) == "\x1b[38;2;80;80;80mfoo\x1b[39m"
        assert wrap("foo", bg=(255, 255, 255)) == "\x1b[48;2;255;255;255mfoo\x1b[49m"

        buf = StringIO()
        with Snazzy("li_red", stream=buf):
            print("foo", file=buf)
        buf.seek(0)
        assert buf.read() == "\x1b[91mfoo\n\x1b[39m"

        # Result depends on platform
        assert emoji("❌", "X")

    def test_coverage(self):
        demo()
