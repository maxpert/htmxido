from . import domx

def test_htmx_processor_handles_camel_and_snake_case():
        assert str(domx.p("Another text", hx_target="foo")) == '<p hx-target="foo">Another text</p>'
        assert str(domx.a("Click", hx_push_url="foo")) == '<a hx-push-url="foo">Click</a>'

        assert str(domx.p("Another text", hxTarget="foo")) == '<p hx-target="foo">Another text</p>'
        assert str(domx.a("Click", hxPushUrl="foo")) == '<a hx-push-url="foo">Click</a>'

        assert str(domx.p(
                domx.span("Hello", hxTest="1"),
                domx.span("World", hxTest="2"),
                hxTest="3"
        )) == '<p hx-test="3"><span hx-test="1">Hello</span><span hx-test="2">World</span></p>'

def test_deferred_content_style():
        assert str(domx.div(class_="test", hxTarget="root")(
                "test"
        )) == '<div class="test" hx-target="root">test</div>'

def test_htmx_generator():
        assert str(domx.ul(
                domx.li(f"Name {i}") for i in range(1, 3)
        )) == '<ul><li>Name 1</li><li>Name 2</li></ul>'

def test_keywords_are_attributed_properly():
        assert str(domx.div(
                "Test",
                class_="large"
        )) == '<div class="large">Test</div>'

        assert str(domx.div(
                "Test",
                with_="large"
        )) == '<div with="large">Test</div>'

def test_example():
        x = domx
        example_dom = x.div(id="root", class_="bg-white dark:bg-slate-800 rounded-lg px-6 py-8 ring-1 ring-slate-900/5 shadow-xl")(
                x.h1(hxIndicator="#spinner")('Hello World'),
                x.p('You can have nested elements like this:'),
                x.ul(
                        x.li(f"Item {i}") for i in range(1, 3)
                ),
                x.div('Not only that but also you can have HTMX attributes'),
                x.button(hxTarget="rubber-band")('Click me'),
                x.img(id="spinner", src="loading.gif", class_="spinner-animation")
        )

        print(str(example_dom))