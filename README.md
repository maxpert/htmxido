# What is htmxido?

HTMXido is declerative HTMX generation library for Python.


## Why?

Since the invent of React SSR (likes of Next.js), people are suddenly excited about writing server side views.
While this method is not new (PHP the grand dad of all), I was looking for something that is very close 
to writing inline code that can generate HTML and process HTMX attributes on those elements.

After looking around and finding a few libraries but none of them were satifactory. So I ended up writing something
for my own self, only to realize it can be reused by more people.

## What does it look like?

```python
import htmxido import domx as x

example_dom = x.div(
    x.h1('Hello World'),
    x.p('You can have nested elements like this:'),
    x.ul(
        x.li(f"Item {i}") for i in range(1, 11)
    ),
    x.div('Not only that but also you can have HTMX attributes'),
    x.button('Click me', hxTarget="rubber-band")
)

print(str(example_dom))
```

Will have following output:
```html
<div><h1>Hello World</h1><p>You can have nested elements like this:</p><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li><li>Item 4</li><li>Item 5</li><li>Item 6</li><li>Item 7</li><li>Item 8</li><li>Item 9</li><li>Item 10</li></ul><div>Not only that but also you can have HTMX attributes</div><button hx-target="rubber-band">Click me</button></div>
```


