#!/usr/bin/env python
"""
This script downloads a collection of image files from on a list of URL
locations and then stores them to a local directory.
"""

import os
import urllib2
from re import sre_compile

SOURCE_FILE = './image-sources.txt'

## Parsing library
TEMPLATE_LINE_RE = sre_compile.compile('^(\w+):(.+)')
URL_LINE_RE = sre_compile.compile('^\w+:/{2}.+')

class Tokens:
    UNDEFINED = 0
    TEMPLATE = 1
    URL = 2

class LineToken:
    """
    Tokenizes an entire line as either a template, a url, or as undefined
    """
    def __init__(self, token, value):
        self.token = token
        self.value = value
    pass

def parse_line(line):
    """
    Parses each line to obtain their token and value pair
    """
    line = line.strip() # incase URL or template lines have leading spaces

    parsed = URL_LINE_RE.match(line) # lines with URL syntax
    if parsed:
        return LineToken(Tokens.URL, parsed.group(0))
    pass

    parsed = TEMPLATE_LINE_RE.match(line) # lines with template syntax
    if parsed:
        return LineToken(Tokens.TEMPLATE, [x.strip().lower() \
               for x in parsed.groups()])
    pass

    return LineToken(Tokens.UNDEFINED, line) # lines with illegal syntax
## End of Parsing library

def download_data(url):
    """
    Downloads file content based on URL location. Currently, the content
    is not being filtered, so in addition to images, other file types can
    be requested.
    """
    s = urllib2.urlopen(url)
    data = s.read()
    s.close()
    return data

def write_file(filepath, data):
    """
    Writes raw data to local file path.
    """
    f = open(filepath, 'wb')
    f.write(data)
    f.close()

def next_filename(rename, counter=0):
    """
    Helper function to insert or append a number to the file name specified
    by the rename parameter. This parameter should be a tuple containing the
    base name and extension. The counter variable should be maintained by the
    calling site.
    """
    filename = rename[0] # base file name
    filename += ('-%d' % counter) if counter else '' # if repeats, append count
    filename += rename[1] # file extension
    return filename

if __name__ == '__main__':
    f = open(SOURCE_FILE) # open file with list of URLs and templates
    counter = 0 # used by 'rename' template to count repeating file names

    # Running states used to back each supported template
    rename = None
    folder = os.getcwd()

    # Start parsing line-by-line, and evaluate after a URL line is encountered
    for line in f.xreadlines():
        line = parse_line(line)

        if line.token == Tokens.URL: # process URL line
            try:
                url = line.value
                filename = next_filename(rename, counter) \
                           if rename else os.path.basename(url)
                filepath = os.path.join(folder, filename)
                write_file(filepath, download_data(url))
                counter += 1
            except Exception as ex:
                print '>> Error: Could not download "%s"' % url
                print '>> Cause: %s' % ex.args[0]
            pass
        elif line.token == Tokens.TEMPLATE: # process template line
            template = line.value[0]
            if template == 'rename':
                rename = line.value[1]
                rename = os.path.splitext(rename) # separate base and extension
                counter = 0 # reset each time a rename template is encountered
            elif template == 'folder':
                folder = line.value[1]
            pass
        elif line.token == Tokens.UNDEFINED: # gracefully handle illegal line
            if len(line.value): # ignore empty lines
                print '>> Error: Illegal syntax encountered in "%s"' % \
                    SOURCE_FILE
                print '>> Cause: Cannot translate "%s"' % \
                    line.value.encode('string_escape')
            pass
        pass
    pass

