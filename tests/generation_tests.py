#!/usr/bin/env python3
#
# Test HTML generation

import html_generator as html

def test_h1():
    assert(html.parse_line('# Header 1') == "<h1>Header 1</h1>\n")

def test_h2():
    assert(html.parse_line('## Header 2') == "<h2>Header 2</h2>\n")

def test_h3():
    assert(html.parse_line('### Header 3') == "<h3>Header 3</h3>\n")

def test_h4():
    assert(html.parse_line('#### Header 4') == "<h4>Header 4</h4>\n")

def test_h5():
    assert(html.parse_line('##### Header 5') == "<h5>Header 5</h5>\n")

def test_h6():
    assert(html.parse_line('###### Header 6') == "<h6>Header 6</h6>\n")

def test_start_link_generation():
    assert(html.parse_line('[https://www.google.com]') == \
           "<a href='https://www.google.com'>https://www.google.com</a> ")

    assert(html.parse_line('[https://www.google.com] is a link') == \
           "<a href='https://www.google.com'>https://www.google.com</a> is a link")

def test_embedded_link_generation():
    assert(html.parse_line('This is a link -> [https://www.google.com] to Google') == \
           "This is a link -> <a href='https://www.google.com'>https://www.google.com</a> to Google")