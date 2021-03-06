#!/usr/bin/env python3
#
# Test HTML generation

from nose.tools import assert_equals
from scribe.parser import Parser

parser = Parser()

def test_h1():
    assert_equals(parser.parse_line('# Header 1'), "<h1>Header 1</h1>\n")

def test_h2():
    assert_equals(parser.parse_line('## Header 2'), "<h2>Header 2</h2>\n")

def test_h3():
    assert_equals(parser.parse_line('### Header 3'), "<h3>Header 3</h3>\n")

def test_h4():
    assert_equals(parser.parse_line('#### Header 4'), "<h4>Header 4</h4>\n")

def test_h5():
    assert_equals(parser.parse_line('##### Header 5'), "<h5>Header 5</h5>\n")

def test_h6():
    assert_equals(parser.parse_line('###### Header 6'), "<h6>Header 6</h6>\n")

def test_hr():
    assert_equals(parser.parse_line('---'), "<hr>")

def test_start_link_generation():
    assert_equals(parser.parse_line('[https://www.google.com](Google)'),
                  "<a href='https://www.google.com'>Google</a>")

    assert_equals(parser.parse_line('[https://www.google.com](Google) is a link'),
                  "<a href='https://www.google.com'>Google</a> is a link")

def test_embedded_link_generation():
    assert_equals(parser.parse_line('This is a link -> [https://www.google.com](Google) to Google'),
                  "This is a link -> <a href='https://www.google.com'>Google</a> to Google")

def test_paragraph_generation():
    parser.generate_tag('')

    assert_equals(parser.generate_tag("This is a paragraph"), "<p>This is a paragraph")
    assert_equals(parser.generate_tag("Second line of the paragraph"), "Second line of the paragraph")
    assert_equals(parser.generate_tag(''), "</p>\n")

    parser.generate_tag('')

    assert_equals(parser.generate_tag('A line with a link > [https://www.google.com](Google)'),
                  "<p>A line with a link > <a href='https://www.google.com'>Google</a>")
    assert_equals(parser.generate_tag(''), "</p>\n")

def test_bold_text_generation():
    assert_equals(parser.parse_line("A line with *bold* text."),
                                    "A line with <b>bold</b> text.")

    assert_equals(parser.parse_line("*Bold text*"), "<b>Bold text</b>")

    assert_equals(parser.parse_line("A *line* with more *bold* text."),
                                    "A <b>line</b> with more <b>bold</b> text.")

def test_italic_text_generation():
    assert_equals(parser.parse_line("A line with **italic** text."),
                                    "A line with <i>italic</i> text.")

    assert_equals(parser.parse_line("**Italic text**"), "<i>Italic text</i>")

    assert_equals(parser.parse_line("A **line** with more **italic** text."),
                                    "A <i>line</i> with more <i>italic</i> text.")

def test_lists():
    assert_equals(parser.parse_line("* A list item"), "<ul><li>A list item</li>")
    assert_equals(parser.parse_line("* [http://www.google.com](Google)"),
                                    "<li><a href='http://www.google.com'>Google</a></li>")

    assert_equals(parser.parse_line("* *A bold item*"), "<li><b>A bold item</b></li>")
    assert_equals(parser.parse_line("* **An italic item**"), "<li><i>An italic item</i></li>")
