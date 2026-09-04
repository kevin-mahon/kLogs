import re
from abc import ABC, abstractmethod


class kFilter(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def filter(self, msg: str) -> bool:
        pass


class kWordFilter(kFilter):
    def __init__(self, exclude: str):
        self.exclude = exclude

    def filter(self, msg: str) -> bool:
        return self.exclude in msg


class kMultiWordFilter(kFilter):
    """True when any of `exclude` is a substring of msg."""

    def __init__(self, exclude: list[str]):
        self.exclude = exclude

    def filter(self, msg: str) -> bool:
        return any(word in msg for word in self.exclude)


class kRegexFilter(kFilter):
    """True when `pattern` matches somewhere in msg."""

    def __init__(self, pattern: str):
        self.pattern = re.compile(pattern)

    def filter(self, msg: str) -> bool:
        return self.pattern.search(msg) is not None


class kAndFilter(kFilter):
    """True only when every child filter matches msg."""

    def __init__(self, *filters: kFilter):
        self.filters = filters

    def filter(self, msg: str) -> bool:
        return all(f.filter(msg) for f in self.filters)


class kOrFilter(kFilter):
    """True when any child filter matches msg."""

    def __init__(self, *filters: kFilter):
        self.filters = filters

    def filter(self, msg: str) -> bool:
        return any(f.filter(msg) for f in self.filters)
