from typing import Any, Sequence, Callable, Tuple, Dict
from collections.abc import Collection
from types import GeneratorType
import keyword
import re

TagPreProcessor = Callable[ [Sequence[Any], Dict[str, Any]], Tuple[Sequence[Any], Dict[str, Any]] ]

capitals_pattern = re.compile(r'(?<!^)(?=[A-Z])')
spaces_pattern = re.compile(r' ')
single_tags = {'area', 'img', 'wbr', 'command', 'link', 'meta', 'embed', 'param', 'source', 'br', 'track', 'input', 'col', 'base', 'hr'}

def kebab_case(s: str) -> str:    
    s = capitals_pattern.sub(' ', s)
    return s.replace('_', ' ').replace(' ', '-').lower()

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

def htmx_pre_processor(*args: Sequence[Any], **kwds: Dict[str, Any]) -> Tuple[Sequence[Any], Dict[str, Any]]:
    ret = {}
    for n, v in kwds.items():
        if n.startswith("hx"):
            ret[kebab_case(n)] = v
        else:
            ret[n] = v
    return (args, ret)

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
    def __init__(self, tag: str, case: str, pre_processor: TagPreProcessor) -> None:
        self.case = case
        self.tag = tag
        self.pre_processor = pre_processor
    
    def __call__(self, *args: [Any], **kwds: Dict[str, Any]) -> Any:
        if self.pre_processor is not None:
            f = self.pre_processor
            args, kwds = f(*args, **kwds)

        self.content = _flatten(args)
        self.attributes = kwds
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
            ret.append(f"/>")
        else:
            ret.append(f"</{self.tag}>")
        
        return ''.join(ret)

class DOM:
    def __init__( self, case: str = 'lower', pre_processor: TagPreProcessor = None) -> None:
        self.case = case
        self.pre_processor = pre_processor
    
    def __getattr__( self, attr ):
        if attr.startswith("__") and attr.endswith("__"):
            raise HTMXError("Bad tag", attr)
        return DOMElement(attr, self.case, self.pre_processor)

domx = DOM(pre_processor=htmx_pre_processor)

class HTMXError(Exception):
    """All our exceptions subclass this."""
    def __str__( self ):
        return self.message