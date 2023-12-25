import keyword
import re
from collections.abc import Collection
from html import escape
from types import GeneratorType
from typing import Any, Sequence, Callable, Tuple, Dict, List, Iterable

TagPreProcessor = Callable[[Sequence[Any], Dict[str, Any]], Tuple[Sequence[Any], Dict[str, Any]]]

capitals_pattern = re.compile(r'(?<!^)(?=[A-Z])')
spaces_pattern = re.compile(r' ')
single_tags = {
    'area', 'img', 'wbr',
    'command', 'link', 'meta',
    'embed', 'param', 'source',
    'br', 'track', 'input',
    'col', 'base', 'hr'
}


def _kebab_case(s: str) -> str:
    s = capitals_pattern.sub(' ', s)
    return s.replace('_', ' ').replace(' ', '-').lower()


def _htmx_pre_processor(*args: Sequence[Any], **kwds: Dict[str, Any]) -> Tuple[Sequence[Any], Dict[str, Any]]:
    ret = {}
    for n, v in kwds.items():
        if n.startswith("hx"):
            ret[_kebab_case(n)] = v
        else:
            ret[n] = v
    return args, ret


def _pre_process_keyword_attrs(*args: Sequence[Any], **kwds: Dict[str, Any]) -> Tuple[Sequence[Any], Dict[str, Any]]:
    ret = {}
    for n, v in kwds.items():
        if n.endswith("_") and keyword.iskeyword(n[:-1]):
            n = n[:-1]
        ret[n] = v
    return args, ret


def _flatten(col: Iterable[Any]) -> List[Any]:
    ret = []
    for c in col:
        if isinstance(c, GeneratorType):
            ret = ret + _flatten(c)
            continue

        if isinstance(c, Collection) and not isinstance(c, str):
            ret = ret + _flatten(c)
            continue

        if c is None:
            continue

        ret.append(c)

    return ret


class DOMElement:
    def __init__(self, tag: str, pre_processor: [TagPreProcessor]) -> None:
        self._tag = tag
        self._pre_processor = pre_processor
        self._content = None
        self._attributes = {}

    def __call__(self, *args: [Any], **kwds: Dict[str, Any]) -> Any:
        for f in self._pre_processor:
            args, kwds = f(*args, **kwds)

        self._attributes.update(kwds)

        if self._content is not None:
            raise HTMXError("Content mutation not allowed")

        if self._tag in single_tags and len(args) > 0:
            raise HTMXError(f"{self._tag} can not have content body")

        if len(args) > 0:
            self._content = _flatten(args)
        return self

    def __str__(self) -> str:
        ret = [f"<{self._tag}"]
        for key, value in self._attributes.items():
            if value is not None:
                ret.append(f" {key}=\"{escape(value)}\"")
            else:
                ret.append(f" {key}")

        if self._tag in single_tags:
            ret.append(" />")
        elif self._content is not None:
            ret.append(">")
            for c in self._content:
                if isinstance(c, DOMElement):
                    ret.append(str(c))
                elif isinstance(c, str):
                    ret.append(escape(c))
                else:
                    raise HTMXError("Unknown type for variable", c)
            ret.append(f"</{self._tag}>")
        else:
            ret.append(f"></{self._tag}>")

        return ''.join(ret)


class DOM:
    def __init__(self, pre_processor: [TagPreProcessor]) -> None:
        self._pre_processor = pre_processor

    def __getattr__(self, tag: str):
        if tag.startswith("__") and tag.endswith("__"):
            raise HTMXError("Bad tag", tag)
        return DOMElement(tag, self._pre_processor)


class HTMXError(Exception):
    def __init__(self, message: str, *args: [Any]) -> None:
        self.args = args
        self.message = message

    def __str__(self):
        return self.message


domx = DOM(pre_processor=[_pre_process_keyword_attrs, _htmx_pre_processor])
