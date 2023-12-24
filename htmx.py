from typing import Any, Sequence, Callable, Tuple, Dict
from collections.abc import Collection
from types import GeneratorType
import keyword
import re

TagPreProcessor = Callable[ [Sequence[Any], Dict[str, Any]], Tuple[Sequence[Any], Dict[str, Any]] ]

capitals_pattern = re.compile(r'(?<!^)(?=[A-Z])')
spaces_pattern = re.compile(r' ')
single_tags = {'area', 'img', 'wbr', 'command', 'link', 'meta', 'embed', 'param', 'source', 'br', 'track', 'input', 'col', 'base', 'hr'}

def escape(text: str) -> str:
    if isinstance( text, str ):
        if '&' in text:
            text = text.replace( '&', '&amp;' )
        if '>' in text:
            text = text.replace( '>', '&gt;' )
        if '<' in text:
            text = text.replace( '<', '&lt;' )
        if '\"' in text:
            text = text.replace( '\"', '&quot;' )
        if '\'' in text:
            text = text.replace( '\'', '&quot;' )

    return text

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
    return (args, ret)

def _pre_process_keyword_conflict_attrs(**kwds: Dict[str, Any]) -> Dict[str, Any]:
    ret = {}
    for n, v in kwds.items():
        if n.endswith("_") and keyword.iskeyword(n[:-1]):
            n = n[:-1]
        ret[n] = v
    return ret

def _flatten(col: Sequence[Any]) -> Sequence[Any]:
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
    def __init__(self, tag: str, pre_processor: TagPreProcessor) -> None:
        self.tag = tag
        self.pre_processor = pre_processor
        self.content = []
        self.attributes = {}
    
    def __call__(self, *args: [Any], **kwds: Dict[str, Any]) -> Any:        
        kwds = _pre_process_keyword_conflict_attrs(**kwds)
        if self.pre_processor is not None:
            f = self.pre_processor
            args, kwds = f(*args, **kwds)

        self.attributes.update(kwds)
        self.content = self.content + _flatten(args)
        return self
    
    def __str__(self) -> str:
        ret = [f"<{self.tag}"]

        for key, value in self.attributes.items():
            if value is not None:
                ret.append(f" {key}=\"{escape(value)}\"")
            else:
                ret.append(f" {key}")

        if len(self.content) > 0:
            ret.append(">")
            for c in self.content:
                if isinstance(c, DOMElement):
                    ret.append(str(c))
                elif isinstance(c, str):
                    ret.append(escape(c))
                else:
                    raise HTMXError("Uknown type for variable", c)
        
        if len(self.content) < 1 and self.tag in single_tags:
            ret.append(f" />")
        else:
            ret.append(f"</{self.tag}>")
        
        return ''.join(ret)

class DOM:
    def __init__(self, pre_processor: TagPreProcessor = None) -> None:
        self.pre_processor = pre_processor
    
    def __getattr__(self, tag: str):
        if tag.startswith("__") and tag.endswith("__"):
            raise HTMXError("Bad tag", tag)
        return DOMElement(tag, self.pre_processor)

domx = DOM(pre_processor=_htmx_pre_processor)

class HTMXError(Exception):
    """All our exceptions subclass this."""
    def __str__( self ):
        return self.message