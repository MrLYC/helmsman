import jmespath
from typing import Any
import re


class JMESPath:
    _compiled = None

    def __init__(self, expr: str):
        self._expr = expr

    def __getitem__(self, item: Any) -> Any:
        cls = self.__class__

        if isinstance(item, int):
            return cls(f"{self._expr}[{item}]")

        return cls(f"{self._expr}.{item}")

    def __call__(self, x: Any) -> Any:
        if self._compiled is None:
            self._compiled = jmespath.compile(self._expr)

        return self._compiled.search(x)

    def __eq__(self, other: Any):
        if isinstance(other, JMESPath):
            return self._expr == other._expr

        def match(x: Any) -> bool:
            return self(x) == other

        return match

    def __ne__(self, other: Any) -> bool:
        if isinstance(other, JMESPath):
            return self._expr == other._expr

        def match(x: Any) -> bool:
            return self(x) != other

        return match

    def __lt__(self, other: Any):
        def match(x: Any) -> bool:
            return self(x) < other

        return match

    def __le__(self, other: Any):
        def match(x: Any) -> bool:
            return self(x) <= other

        return match

    def __gt__(self, other: Any):
        def match(x: Any) -> bool:
            return self(x) > other

        return match

    def __ge__(self, other: Any):
        def match(x: Any) -> bool:
            return self(x) >= other

        return match

    def regexp(self, pattern: str):
        re_pattern = re.compile(pattern)

        def match(x: Any) -> bool:
            return re_pattern.search(self(x)) is not None

        return match

    def is_none(self):
        def match(x: Any) -> bool:
            return self(x) is None

        return match

    def is_not_none(self):
        def match(x: Any) -> bool:
            return self(x) is not None

        return match
