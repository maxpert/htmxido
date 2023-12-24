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


def test_htmx_generator():
        assert str(domx.ul(
                domx.li(f"Name {i}") for i in range(1, 3)
        )) == '<ul><li>Name 1</li><li>Name 2</li></ul>'