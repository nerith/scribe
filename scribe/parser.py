import re

class Parser:
    ''' The Parser class represents a parser that parses text using specified
    markup. Once the parser parses the text, HTML is generated as output.
    '''

    def __init__(self):
        self.written_text = ''
        self.remaining_text = ''
        self.markup = { 'h1': '^[#]{1}(\s*)',
                        'h2': '^[#]{2}(\s*)',
                        'h3': '^[#]{3}(\s*)',
                        'h4': '^[#]{4}(\s*)',
                        'h5': '^[#]{5}(\s*)',
                        'h6': '^[#]{6}(\s*)',
                        'hr': '^-{3}',
                        'a': '((\[https?:\/{2}.+?\.(\w+)\])(\(.+?\)))',
                        'b': '(\*).+?(\*)',
                        'i': '(\*\*).+?(\*\*)',
                        'li': '^\*\s{1}',
                      }

        self.header = False
        self.lists = False
        self.in_paragraph = False
        self.previous_line = None

    def get_tags(self):
        ''' Return the available markup symbols '''

        for tag in sorted(self.markup)[::-1]:
            yield tag

    def generate_paragraph(self, text):
        ''' Check if a line starts or ends a paragraph

        A paragraph is currently determined by blank lines separating
        a block of text.
        '''

        if self.previous_line == '' and text != '' and not self.header:
            self.in_paragraph = True
            if not self.lists:
                return_text = "<p>" + text
            else:
                return_text = text
        elif self.previous_line != '' and text == '' and self.in_paragraph:
            self.in_paragraph = False
            return_text = ""

            if self.lists:
                return_text = "\n</ul>"

            else:
                return_text = "</p>\n"
        else:
            return_text = text

        self.previous_line = text

        return return_text

    def generate_tag(self, line):
        ''' Generate a tag

        Parameters:
          line: the line to generate HTML from
        '''

        self.header = False

        text = self.generate_paragraph(self.parse_line(line.replace('\n', '')))

        return text

    def parse_line(self, text):
        ''' Parse a line recursively for markup symbols

        Parameters:
          text: a textual line
        Returns: the generated HTML
        '''

        self.written_text = text
        self.remaining_text = ''

        for key in self.get_tags():
            match = re.search(self.markup[key], text)

            if match:
                start = match.start(0)

                if key == 'hr':
                    self.written_text = '<hr>'
                elif key == 'b' or key == 'i':
                    inner_text = "<{}>{}</{}>".format(key, text[match.end(1):match.start(2)], key)

                    if start > 0:
                        self.written_text = text[:start] + inner_text
                    else:
                        self.written_text = inner_text

                    self.remaining_text = text[match.end(len(match.groups())):]
                elif key == 'li':
                    if not self.lists:
                        self.lists = True
                        some_text = "<ul>"
                    else:
                        some_text = ""

                    self.remaining_text = text[2:]
                    self.written_text = "{}<{}>{}</{}>".format(some_text, key, self.parse_line(self.remaining_text), key)
                elif key != 'a':
                    self.remaining_text = text[match.span()[1]:]
                    self.written_text = "<{}>{}</{}>\n".format(key, self.parse_line(self.remaining_text), key)

                    self.header = True
                elif key == 'a':
                    link_name = match.groups()[1].replace('[', '').replace(']', '')
                    link_title = match.groups()[3].replace('(', '').replace(')', '')

                    link = "<a href='{}'>{}</a>"

                    # Check where the link is within the line
                    if match.start(0) > 0:
                        self.written_text = text[:start] + link.format(link_name, link_title)
                    else:
                        self.written_text = link.format(link_name, link_title)

                    self.remaining_text = text[match.end(len(match.groups())):]

                break

        if self.remaining_text == '':
            return self.written_text

        return self.written_text + self.parse_line(self.remaining_text)
