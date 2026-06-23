"""A small recursive-descent parser for Minecraft's SNBT (stringified NBT).

SNBT is JSON-like but not JSON: keys are usually unquoted, scalars carry type
suffixes (``0b`` byte, ``0s`` short, ``0L`` long, ``0.5f`` float, ``0.5d``
double), and there are typed arrays (``[I; 1, 2, 3]``, ``[B; ...]``, ``[L; ...]``).

We only need to read it, so values decay to plain Python types:
compound -> dict, list/array -> list, string -> str, integral -> int,
floating -> float, ``true``/``false`` -> 1/0. That is everything the
translators consume; no typed wrappers are required.
"""

from __future__ import annotations

import re

_INT_RE = re.compile(r"[+-]?\d+$")
_FLOAT_RE = re.compile(r"[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?$")
_STOPPERS = " \t\r\n,{}[]"
_KEY_STOPPERS = " \t\r\n:{}[],"


class SNBTError(ValueError):
    """Raised when a string cannot be parsed as SNBT."""


def parse(text: str):
    """Parse an SNBT string into plain Python types."""
    return _Parser(text).parse()


class _Parser:
    def __init__(self, text: str):
        self.s = text
        self.i = 0
        self.n = len(text)

    def parse(self):
        self._ws()
        value = self._value()
        self._ws()
        if self.i != self.n:
            raise SNBTError(f"trailing data at position {self.i}")
        return value

    def _value(self):
        self._ws()
        c = self._peek()
        if c == "":
            raise SNBTError("unexpected end of input")
        if c == "{":
            return self._compound()
        if c == "[":
            return self._list()
        if c in "\"'":
            return self._quoted(c)
        return self._literal()

    def _compound(self) -> dict:
        obj: dict = {}
        self.i += 1  # consume '{'
        self._ws()
        if self._peek() == "}":
            self.i += 1
            return obj
        while True:
            self._ws()
            key = self._key()
            self._ws()
            self._expect(":")
            obj[key] = self._value()
            self._ws()
            c = self._next()
            if c == ",":
                continue
            if c == "}":
                return obj
            raise SNBTError(f"expected ',' or '}}' near position {self.i}")

    def _list(self) -> list:
        self.i += 1  # consume '['
        self._ws()
        # Typed array prefix: 'I;', 'B;', or 'L;'. The element type doesn't
        # change how we store values (always a list), so just skip the prefix.
        if self._peek() in "IBL" and self._peek(1) == ";":
            self.i += 2
        return self._items()

    def _items(self) -> list:
        items: list = []
        self._ws()
        if self._peek() == "]":
            self.i += 1
            return items
        while True:
            items.append(self._value())
            self._ws()
            c = self._next()
            if c == ",":
                continue
            if c == "]":
                return items
            raise SNBTError(f"expected ',' or ']' near position {self.i}")

    def _key(self) -> str:
        c = self._peek()
        if c in "\"'":
            return self._quoted(c)
        start = self.i
        while self.i < self.n and self.s[self.i] not in _KEY_STOPPERS:
            self.i += 1
        if self.i == start:
            raise SNBTError(f"empty key near position {self.i}")
        return self.s[start:self.i]

    def _quoted(self, quote: str) -> str:
        self.i += 1  # opening quote
        chars = []
        while self.i < self.n:
            c = self.s[self.i]
            if c == "\\":
                self.i += 1
                if self.i < self.n:
                    chars.append(self.s[self.i])
                    self.i += 1
                continue
            if c == quote:
                self.i += 1
                return "".join(chars)
            chars.append(c)
            self.i += 1
        raise SNBTError("unterminated string")

    def _literal(self):
        start = self.i
        while self.i < self.n and self.s[self.i] not in _STOPPERS:
            self.i += 1
        token = self.s[start:self.i]
        if token == "":
            raise SNBTError(f"empty value near position {self.i}")
        return _interpret(token)

    def _peek(self, ahead: int = 0) -> str:
        j = self.i + ahead
        return self.s[j] if j < self.n else ""

    def _next(self) -> str:
        c = self._peek()
        self.i += 1
        return c

    def _expect(self, ch: str):
        if self._peek() != ch:
            raise SNBTError(f"expected {ch!r} near position {self.i}")
        self.i += 1

    def _ws(self):
        while self.i < self.n and self.s[self.i] in " \t\r\n":
            self.i += 1


def _interpret(token: str):
    low = token.lower()
    if low == "true":
        return 1
    if low == "false":
        return 0
    suffix = token[-1]
    body = token[:-1]
    if suffix in "bBsSlL" and _INT_RE.match(body):
        return int(body)
    if suffix in "fFdD" and _FLOAT_RE.match(body):
        return float(body)
    if _INT_RE.match(token):
        return int(token)
    if _FLOAT_RE.match(token):
        return float(token)
    return token  # unquoted string
