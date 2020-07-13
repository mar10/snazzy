# snazzy

> Stylish ANSI terminal colors and helpers.

[![Build Status](https://travis-ci.org/mar10/snazzy.svg?branch=master)](https://travis-ci.org/mar10/snazzy)
[![Latest Version](https://img.shields.io/pypi/v/snazzy.svg)](https://pypi.python.org/pypi/snazzy/)
[![License](https://img.shields.io/pypi/l/snazzy.svg)](https://github.com/mar10/snazzy/blob/master/LICENSE)
[![Coverage Status](https://coveralls.io/repos/github/mar10/snazzy/badge.svg?branch=master)](https://coveralls.io/github/mar10/snazzy?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![StackOverflow: snazzy](https://img.shields.io/badge/StackOverflow-snazzy-blue.svg)](https://stackoverflow.com/questions/tagged/snazzy)

## Usage

```py
from snazzy import enable_colors, green, wrap

enable_colors()

print("That looks " + green("good") + ", right?")
print(emoji(" ✨ 🍰 ✨", ":-)"))
```

![looks good](https://github.com/mar10/snazzy/raw/master/tests/that_looks_good.png)

Note two things:

1. *snazzy* is inactive by default, so we have to call `enable_colors()` first.
2. The function `green(<text>)` wraps the text in ANSI escape sequences to apply
   green foreground color and reset to the default color afterwards.

The function `green(<text>)` is only a convenience shortcut for `wrap(<text>, ...)`:

```py
assert green("good") == wrap("good", fg="green")
```

However `wrap()` is more powerful and flexible, since it also allows to set background
color and attributes (bold, italic, underline):

```py
print(wrap("white on blue", "white", bg="blue"))
print(wrap("ERROR:", "yellow", bg="red", bold=True) + " that went wrong.")
```

Alternative pattern, using a context manager:

```py
with Snazzy(fg="green", bg="black"))
    print("This is so eighties...")
```

The context manager pattern is syntactic sugar for for this explicit code:

```py
print(ansi("green", bg="black"), end="")
print("This is so eighties...")
print(ansi_reset(), end="")
```

### Available Formats

#### Colors

Color keys can be used as foreground or background using the `fg=COLOR` and
`bg=COLOR` option respectively.<br>
**Note:** Not all platforms implement all features
[see here for an overview](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors).

These are well supported in most terminals:

`"black"`, `"red"`, `"green"`, `"yellow"`, `"blue"`, `"magenta"`, `"cyan"`, `"white"`.

These are less good supported:

`"li_black"`, `"li_red"`, `"li_green"`, `"li_yellow"`, `"li_blue"`, `"li_magenta"`,
`"li_cyan"`, `"li_white"`.

These are less supported:

`"da_black"`, `"da_red"`, `"da_green"`, `"da_yellow"`, `"da_blue"`, `"da_magenta"`,
`"da_cyan"`, `"da_white"`.

We can also pass *RGB* tuples like so if the platform supports it:
```py
print(wrap("white on blue", (255, 255, 255), bg=(0, 0, 200)))
```

#### Effects

The following effects are available:

`"bold"`, `"dim"`, `"italic"`, `"underline"`, `"blink"`, `"inverse"`, `"hidden"`,
`"strike"`.

(`"b"`, `"i"`, and `"u"` may be used as alias for bold, italic, and underline.)

#### Format Reset

The following codes reset distinct formattings to default values:

`"reset_all"`, `"reset_fg"`, `"reset_bg"`, `"reset_bold_dim"`, `"reset_italic"`,
`"reset_underline"`, `"reset_blink"`, `"reset_inverse"`, `"reset_hidden"`,
`"reset_strike"`.

(The `wrap()` methods appends this automatically to the wrapped text.)

### Enable Colors

*Snazzy* is disabled by default, because not all terminals and platforms support
ANSI codes, resulting in ugly text.<br>
Also, when output is redirected to log files, we want to suppress those escape
sequences.<br>
Finally, a command line tool that uses `snazzy` might want to offer a
command line argument `--no-color` to disable colors:

```py
if not args.no_color:
    snazzy.enable_colors()
```

Until explicitly enabled, no escape sequencrs are generated, so the the wrappers
behave transparently:

```py
from snazzy import red, enable_colors

assert red("error") == "error"

enable_colors(True)
assert red("error") == "\x1b[91merror\x1b[39m"
```

### Emojis

The `emoji(s, fallback)` method allows to emit emojis and other fancy unicode
characters, but fallback to a replacement string if the terminal does not
support this.

```py
print("{} this is a bug.".format(emoji("❌", red("X"))))
print(emoji("✨ 🍰 ✨", ":-)"))
```

**Note:** Currently we assume that Windows does not support emojis, but
other terminals do.
