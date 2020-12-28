# -*- coding: utf-8 -*-
# (c) 2020 Martin Wendt and contributors; see https://github.com/mar10/snazzy
# Licensed under the MIT license: https://www.opensource.org/licenses/mit-license.php
"""
Stylish ANSI terminal colors and helpers.

Examples:
    from snazzy import enable_colors, red

    if not args.no_color:
        enable_colors(True)
    print(red("foo"))
"""
import os
import re
import sys

__version__ = "0.2.3-a1"


ANSI_ESCAPE_8BIT_STR = re.compile(
    r"(?:\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])"
)
ANSI_ESCAPE_8BIT_BYTES = re.compile(
    br"(?:\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])"
)


# Foreground ANSI codes using SGR format:
_SGR_FG_COLOR_MAP = {
    "reset_all": 0,
    "reset_fg": 39,
    # These are well supported.
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
    # These are less good supported.
    "li_black": 90,
    "li_red": 91,
    "li_green": 92,
    "li_yellow": 93,
    "li_blue": 94,
    "li_magenta": 95,
    "li_cyan": 96,
    "li_white": 97,
}

FG_MAP = {color: "\033[{}m".format(num) for color, num in _SGR_FG_COLOR_MAP.items()}

# Background ANSI codes using SGR format:
_SGR_BG_COLOR_MAP = {
    "reset_bg": 49,
    # These are well supported.
    "black": 40,
    "red": 41,
    "green": 42,
    "yellow": 43,
    "blue": 44,
    "magenta": 45,
    "cyan": 46,
    "white": 47,
    # These are less good supported.
    "li_black": 100,
    "li_red": 101,
    "li_green": 102,
    "li_yellow": 103,
    "li_blue": 104,
    "li_magenta": 105,
    "li_cyan": 106,
    "li_white": 107,
}

BG_MAP = {color: "\033[{}m".format(num) for color, num in _SGR_BG_COLOR_MAP.items()}

# ANSI codes using 8-bit format (used for fore- and background)

_BIT_COLOR_MAP = {
    # These are less supported.
    "da_black": 0,
    "da_red": 88,
    "da_green": 22,
    "da_yellow": 58,
    "da_blue": 18,
    "da_magenta": 89,
    "da_cyan": 23,
    "da_white": 249,
}

FG_MAP.update(
    {color: "\033[38;5;{}m".format(num) for color, num in _BIT_COLOR_MAP.items()}
)
BG_MAP.update(
    {color: "\033[48;5;{}m".format(num) for color, num in _BIT_COLOR_MAP.items()}
)


_SGR_EFFECT__MAP = {
    # Reset distinct effects
    "reset_all": 0,
    "reset_fg": 39,
    "reset_bg": 49,
    "reset_bold_dim": 22,
    "reset_dim_bold": 22,
    "reset_i": 23,
    "reset_italic": 23,
    "reset_u": 24,
    "reset_underline": 24,
    "reset_blink": 25,
    "reset_inverse": 27,
    "reset_hidden": 28,
    "reset_strike": 29,
    # Effects
    "b": 1,
    "bold": 1,
    "dim": 2,
    "i": 3,
    "italic": 3,
    "u": 4,
    "underline": 4,
    "blink": 5,
    "inverse": 7,
    "hidden": 8,
    "strike": 9,
}
EFFECT_MAP = {color: "\033[{}m".format(num) for color, num in _SGR_EFFECT__MAP.items()}


def rgb_fg(r, g, b):
    return "\x1b[38;2;{};{};{}m".format(r, g, b)


def rgb_bg(r, g, b):
    return "\x1b[48;2;{};{};{}m".format(r, g, b)


class Snazzy:
    """
    This is basically a namespace, since the core functionality is implemented
    as classmethods.

    However an instance is required to use a context manager.
    Examples:

        with Snazzy("yellow", bg="blue"):
            print("hey")

    """

    #: (bool) True if Snazzy feature detection was run and initialion finished
    _initialized = False
    #: (bool) True if `enable(True)` was called
    _enabled = False
    #: (bool) True if the terminal supports fancy unicode
    _support_emoji = None

    def __init__(
        self, fg=None, bg=None, bold=False, underline=False, italic=False, stream=None
    ):
        self.format = (fg, bg, bold, underline, italic)
        self.stream = stream

    def __enter__(self):
        print(self.ansi(*self.format), end="", file=self.stream)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Note: if the previous output (inside the context manager) ended
        # with `\n`, the next line may already be painted in the background color,
        # so resetting might not work as expected.
        # Caller could do an additional `print()` to fix this.
        print(self.reset(*self.format), end="", file=self.stream)

    @classmethod
    def _initialize(cls):
        """"""
        if cls._initialized:
            return
        cls._initialized = True
        # Shim to make colors work on Windows 10
        # See https://github.com/feluxe/sty/issues/2
        if sys.platform == "win32":
            os.system("color")

        # TODO: this is an overly simple guess.
        cls._support_emoji = True
        if not cls._initialized:
            cls._support_emoji = False
        elif sys.platform == "win32":
            # Windows CMD and Powershell don't support emojis, but 'Windows Terminal' does
            if not os.environ.get("WT_SESSION"):
                cls._support_emoji = False
        return

    # TODO:
    # https://docs.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences

    @classmethod
    def enable(cls, flag, force=False, support_emoji=None):
        """Set 'enabled'-status.

        Args:
            flag (bool):
            force (bool): True: enable even if isatty() is false
            support_emoji (bool, optional):
        """
        if flag and not force and not sys.stdout.isatty():
            flag = False

        if flag:
            cls._initialize()
        cls._enabled = flag
        if support_emoji is not None:
            cls._support_emoji = support_emoji

    @classmethod
    def is_enabled(cls):
        return cls._enabled

    @classmethod
    def reset_all(cls):
        return EFFECT_MAP.get("reset_all")

    @classmethod
    def reset(cls, fg=True, bg=True, bold=True, underline=True, italic=True):
        if not cls._enabled:
            return ""
        if fg and bg and bold and underline and italic:
            return cls.reset_all()

        sl = []
        if fg:
            sl.append(EFFECT_MAP["reset_fg"])
        if bg:
            sl.append(EFFECT_MAP["reset_bg"])
        if bold:
            sl.append(EFFECT_MAP["reset_bold_dim"])
        if italic:
            sl.append(EFFECT_MAP["reset_italic"])
        if underline:
            sl.append(EFFECT_MAP["reset_underline"])
        res = "".join(sl)
        return res

    @classmethod
    def ansi(cls, fg=None, bg=None, bold=False, underline=False, italic=False):
        if not cls._enabled:
            return ""
        sl = []

        if fg is not None:
            # TODO: in simple cases, fg and bg can be combined into a single sequence
            if isinstance(fg, (list, tuple)):
                sl.append(rgb_fg(*fg))
            else:
                sl.append(FG_MAP[fg])

        if bg is not None:
            if isinstance(bg, (list, tuple)):
                sl.append(rgb_bg(*bg))
            else:
                sl.append(BG_MAP[bg])
        # Effects
        if bold:
            sl.append(EFFECT_MAP["bold"])
        if underline:
            sl.append(EFFECT_MAP["underline"])
        if italic:
            sl.append(EFFECT_MAP["italic"])
        return "".join(sl)

    @classmethod
    def wrap(cls, text, fg=None, bg=None, bold=False, underline=False, italic=False):
        """Return a colorized text using ANSI escape codes.

        See also: https://en.wikipedia.org/wiki/ANSI_escape_code

        When
        Examples:
            print("Hello " + color("beautiful", "green") + " world.")
        """
        if not cls._enabled:
            return text
        sl = []
        sl.append(cls.ansi(fg=fg, bg=bg, bold=bold, underline=underline, italic=italic))
        if text is not None:
            sl.append(text)
            # Only reset what we have set before
            sl.append(
                cls.reset(fg=fg, bg=bg, bold=bold, underline=underline, italic=italic)
            )

        text = "".join(str(s) for s in sl)
        return text

    @classmethod
    def cleanup(cls, s):
        """Remove 7-bit and 8-bit C1 ANSI sequences."""
        if isinstance(s, str):
            res = ANSI_ESCAPE_8BIT_STR.sub("", s)
        else:
            res = ANSI_ESCAPE_8BIT_BYTES.sub(b"", s)
        return res

    @classmethod
    def emoji(cls, s, fallback="", force=None):
        """Return an emoji-string if the terminal supports it, fallback otherwise."""
        enable = cls._support_emoji if force is None else force
        return s if enable else fallback

    # @classmethod
    # def set_cursor(cls, x, y, apply=True):
    #     # https://docs.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences
    #     if not cls._enabled:
    #         return ""
    #     ansi = ""
    #     if apply:
    #         print(ansi, end="")
    #     return ansi


def enable_colors(flag=True, force=False):
    return Snazzy.enable(flag, force)


def colors_enabled():
    return Snazzy.is_enabled()


def cleanup_ansi_codes(s):
    """Remove 7-bit and 8-bit C1 ANSI sequences."""
    return Snazzy.cleanup(s)


def emoji(s, fallback="", force=None):
    """Return an emoji-string if the terminal supports it, fallback otherwise."""
    return Snazzy.emoji(s, fallback, force)


def ansi_reset(fg=True, bg=True, bold=True, underline=True, italic=True):
    """Reset color attributes to console default."""
    return Snazzy.reset(fg, bg, bold, underline, italic)


def ansi(fg=None, bg=None, bold=False, underline=False, italic=False):
    """Return ANSI control string that enables the requested console formatting."""
    return Snazzy.ansi(fg, bg, bold, underline, italic)


def wrap(text, fg=None, bg=None, bold=False, underline=False, italic=False):
    """Wrap text in ANSI sequences that enable and disable console formatting."""
    return Snazzy.wrap(text, fg, bg, bold, underline, italic)


# def set_cursor(x, y):
#     return Snazzy.set_cursor(x, y)


def red(text):
    return wrap(text, "li_red")


def yellow(text):
    return wrap(text, "li_yellow")


def green(text):
    return wrap(text, "green")


def gray(text):
    return wrap(text, "li_black")


def demo():
    def _dump(title, fg_color, bg_color):
        COLUMNS = 8
        sl = []
        for color in FG_MAP.keys():
            if "reset" in color:
                continue
            prefix = "\n" if len(sl) % COLUMNS == 0 else ""
            fg = color if fg_color == "*" else fg_color
            bg = color if bg_color == "*" else bg_color
            text = "{:<10}".format(color)
            text = wrap(text, fg=fg, bg=bg)
            sl.append(prefix + wrap(text, color))

        print(wrap(title, "li_white", bold=True, underline=True), end="")
        print(", ".join(sl))
        print(Snazzy.reset_all())

    enable_colors(True)

    _dump("Foreground colors:", "*", None)
    _dump("Background colors:", "black", "*")

    sl = []
    sl.append(wrap("bold", bold=True))
    sl.append(wrap("italic", italic=True))
    sl.append(wrap("underline", underline=True))
    print(wrap("Effects", "li_white", bold=True, underline=True))
    print("{}".format(", ".join(sl)))
    print()

    print("That looks " + green("good") + ", right?")
    print(wrap("ERROR:", "li_yellow", bg="red", bold=True) + " This is an error?")

    with Snazzy("yellow", bg="black"):
        print("This is so eighties...")
    print()

    # with Snazzy("li_yellow", bg="blue"):
    #     print("yellow on blue")
    # print()

    # with Snazzy((255, 255, 0), bg=(0, 0, 255)):
    #     print("yellow on blue (rgb)")

    # with Snazzy("li_white", bg="black"):
    #     print("white on black")

    # with Snazzy((255, 255, 255), bg="black"):
    #     print("white on black (rgb)")

    # # print("before " + red("reddish") + " after")
    # # print("before " + yellow("yellow") + " after")
    # print("before " + wrap("yellow on blue", "yellow", bg="blue") + " after")
    # print("before " + wrap("green underlined", "green", underline=True) + " after")
    # print("before " + wrap("blue bold", "blue", bold=True) + " after")
    # print("before " + wrap("red italic", "red", italic=True) + " after")


if __name__ == "__main__":
    demo()
