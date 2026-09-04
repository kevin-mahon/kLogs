import re
from abc import ABC, abstractmethod


class kFilter(ABC):
    """Base class for message filters.

    filter(msg) returns True when msg matches this filter's condition,
    meaning the message should be *excluded* from log output. This is
    the opposite of stdlib logging.Filter, where True means *keep* the
    record — see kLogger.addFilter, which bridges the two.
    """

    def __init__(self):
        pass

    @abstractmethod
    def filter(self, msg: str) -> bool:
        pass

    def __and__(self, other: "kFilter | str") -> "kAndFilter":
        return kAndFilter(self, as_filter(other))

    def __rand__(self, other: "kFilter | str") -> "kAndFilter":
        return kAndFilter(as_filter(other), self)

    def __or__(self, other: "kFilter | str") -> "kOrFilter":
        return kOrFilter(self, as_filter(other))

    def __ror__(self, other: "kFilter | str") -> "kOrFilter":
        return kOrFilter(as_filter(other), self)


def as_filter(value: "kFilter | str") -> kFilter:
    """Coerce a bare string into a kWordFilter; pass kFilters through unchanged."""
    return kWordFilter(value) if isinstance(value, str) else value


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
