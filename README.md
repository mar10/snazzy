# snazzy

> Stylish ANSI terminal colors.

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
```

That looks <span style="color: green;">good</span>, right?

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

Alternative pattern 'context manager':

```py
with Snazzy(fg="green", bg="black"))
    print("This is so eighties...")
```

Alternative pattern 'explicit':

```py
print(ansi("green", bg="black"), end="")
print("This is so eighties...")
print(ansi_reset(), end="")
```

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

enable_colors(True, True)
assert red("error") == "\x1b[91merror\x1b[39m"
```
