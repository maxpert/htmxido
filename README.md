# What is htmxido?

HTMXido is declerative HTMX generation library for Python.

[![codecov](https://codecov.io/gh/maxpert/htmxido/graph/badge.svg?token=ULBG6B8R39)](https://codecov.io/gh/maxpert/htmxido)

## Install

```
pip install htmxido
```

## Why?

Since the invention of React SSR (like Next.js), there has been newfound enthusiasm for writing server-side views. Although this method isn't new (consider PHP, the grandfather of all), I was searching for a solution close to writing inline code capable of generating HTML and processing HTMX attributes on those elements.

After exploring various libraries and finding them unsatisfactory, I ended up creating something for myself. It later dawned on me that it could benefit more people.

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

As much as people hated PHP and made fun of it, with the invention of HTMX, it has become evident that building medium-sized applications in React is bloated (as React was intended for smaller parts of the page). The effort engineers put into basic tasks that could be accomplished by merely sending back HTML from the server was underestimated.

While you might be averse to the idea of replacing .innerHTML the old-school way, it turns out you can achieve a lot with just HTMX and jQuery-like declarative DOM ([here is an example](https://www.youtube.com/watch?v=3GObi93tjZI)).

Now, there are a few excellent aspects that backend developers will truly appreciate about htmxido:

 - **It's all Python** - This means it runs fast! You can use existing tooling and linters.
 - **Lazy evaluated** - Unless you serialize your DOM (with conversion to str), it remains a DOM! This implies that you can cache for even more speed.
 - **Functional components** - You can easily envision view functions returning these DOM elements that can be reused across requests.

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

### More usage examples:

Here is an example app Sanic:

```python
from sanic import Sanic, html
from htmxido import domx as x

app = Sanic("Pythia")

@app.post("/clicked")
async def clicked(request):
    return html(str(
        x.div("Clicked!!!")
    ))

@app.get("/")
async def home(request):
    return html(str(
        x.html(
            x.head(
                x.script(src="https://unpkg.com/htmx.org@1.9.9")
            ),
            x.body(
                x.h1("Running htmxido"),
                x.div(id="container")(
                    x.button("Reveal!!!", hxTarget="#container", hxTrigger="click", hxPost="/clicked")
                ),
            )
        )
    ))
```

## Contributing

I use pytest for testing, and coverage for coverage report. You can simply run tests by:

```sh
coverage run -m pytest && coverage html && open htmlcov/index.html
```
