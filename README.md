# What is htmxido?

HTMXido is declerative HTMX generation library for Python.

## Install

```
pip install htmxido
```

## Why?

Since the invent of React SSR (likes of Next.js), people are suddenly excited about writing server side views.
While this method is not new (PHP the grand dad of all), I was looking for something that is very close 
to writing inline code that can generate HTML and process HTMX attributes on those elements.

After looking around and finding a few libraries but none of them were satifactory. So I ended up writing something
for my own self, only to realize it can be reused by more people.

## What does it look like?

```python
from htmxido import domx as x

example_dom = x.div(id="root", class_="bg-white dark:bg-slate-800 rounded-lg px-6 py-8 ring-1 ring-slate-900/5 shadow-xl")(
    x.h1(hxIndicator="#spinner")('Hello World'),
    x.p('You can have nested elements like this:'),
    x.ul(
        x.li(f"Item {i}") for i in range(1, 3)
    ),
    x.div('Not only that but also you can have HTMX attributes'),
    x.button(hxTarget="rubber-band")('Click me')
    x.img(id="spinner", src="loading.gif", class_="spinner-animation")
)

print(str(example_dom))
```

**NOTE**: Any keyword attributes should be suffixed with `_`, and they will be removed as per showin in following output.

```html
<div id="root" class="bg-white dark:bg-slate-800 rounded-lg px-6 py-8 ring-1 ring-slate-900/5 shadow-xl">
    <h1 hx-indicator="#spinner">Hello World</h1>
    <p>You can have nested elements like this:</p>
    <ul><li>Item 1</li><li>Item 2</li></ul>
    <div>Not only that but also you can have HTMX attributes</div>
    <button hx-target="rubber-band">Click me</button>
    <img id="spinner" src="loading.gif" class="spinner-animation"/>
</div>
```

## So I can write views like code, what's the big deal?

As much as people hated PHP and made fun of it. With the invent of HTMX it has become very obvious that writing medium sized 
applications in React is bloated (because react was supposed to do small parts of page), and effort engineers are spending 
for basic stuff that can be done by simply sending back HTML from server is something everyone under-estimated. While you
might be digusted by the idea of replacing a `.innerHTML` the old school way, turns you can do a lot with just HTMX
and jQuery aged declarative DOM ([here is an example](https://www.youtube.com/watch?v=3GObi93tjZI)). 

Now there are two beautiful parts that backend developers will really appriciate about htmxido:

 - **It's all Python** - Which means you it runs fast! You can use existing tooling, and linters.
 - **Lazy evaluated** - Unless you serialize your DOM (with conversion to `str`), it remains DOM! Which means you can cache for even more speed.
 - **Functional components** - You can easily think view functions returning you these DOM elements that can be reused across requests.

So in a nutshell you can do something like this:

```python
from htmxido import DOMElement, domx

## Imagine more functional components here

## For this example let's imagine we want to render a header component with hamburger menu.
@cached(ttl=3600)
def header(account: AccountInfo) -> DOMElement:
    """
    Returns header DOM component for given element account info
    """
    return domx.div(class_="nav-bar full-width responsive")(
        domx.h1(f"Welcome {account.name}"),
        hamburger(account) # Reusing another component
    )
```