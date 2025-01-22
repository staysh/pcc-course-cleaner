from bs4 import BeautifulSoup as soup
import os
import sys
import re
import argparse
import pathlib

parser = argparse.ArgumentParser(description='Clean a Brightspace package')
parser.add_argument('-f', '--folder', type=pathlib.Path,
                    required=True, help='path to unzipped package')
parser.add_argument('-l', '--links', action='store_true',
                    help='option for all links to open new window')
parser.add_argument('-s', '--sheet', action='store',
                    default='/shared/css/8.0/css/stylesheet.css',
                    nargs='?', help='d2l path to stylesheet')
parser.add_argument('-k', '--keep', nargs='?',
                    help='keywords in stylesheet paths to keep ("bootstrap" for instance)')
parser.add_argument('-c', '--clean', action='store_true',
                    help='option to clean non-layout style')
parser.add_argument('-d', '--debug', action='store_true',
                    help='debug mode or dry run')


args = parser.parse_args()
no_float = re.compile("^(?:(?!float).)*$\r?\n?")
ext = re.compile("\.html?$")

if os.path.isdir(args.folder):
    for root, dirs, files in os.walk(args.folder):
        for name in files:
            # clean html files of style attr and span tags
            # optionally remove linked css and replace with template
            if ext.search(name):
                full_path = os.path.join(root, name)
                if args.debug:
                    print('HTML File Found: ' + str(full_path))
                with open(full_path, "r+") as html:
                    doc = soup(html.read(), "html.parser")
                    # get all link elements from head
                    css = doc.find_all("link", rel="stylesheet")
                    for ss in css:
                        # delete old ss
                        # perhaps check for bootstrap or shared cond. delete
                        if args.keep:
                            if not args.keep.lower() in ss['href'].lower():
                                if args.debug:
                                    print('Not Keeping Stylesheet: ' + ss['href'])
                                else:
                                    ss.decompose()
                            else:
                                print('Keeping Stylesheet: ' + ss['href'])
                        else:
                            if args.debug:
                                print('Not Keeping Stylesheet: ' + ss['href'])
                            else:
                                ss.decompose()
                    # insert latest template css (could be an arg)
                    if args.debug:
                        print('Inserting Stylesheet: ' + args.sheet)
                    else:
                        if doc.head:
                            new_css = doc.new_tag(name="link", rel="stylesheet", href=args.sheet, type="text/css")
                            doc.head.append(new_css)
                    # clear spans preserve inner data
                    if args.clean or args.debug:
                        spans = doc.find_all("span")
                        count_spans = 0
                        for span in spans:
                            count_spans += 1
                            if not args.debug:
                                span.unwrap()
                        # find all style that doesn't reference layout aka float
                        tags = doc.find_all(style=no_float)
                        count_inline = 0
                        for tag in tags:
                            # also avoid these items (generally don't have font props)
                            # perhaps switch to affirmative prop delete from list of bad props?
                            # color, font size/family, etc
                            if tag.name not in ['img', 'div', 'ol', 'iframe', 'ul']:
                                count_inline += 1
                                if not args.debug:
                                    del tag['style']
                    # clean links to open in new window
                    if args.links or args.debug:
                        links = doc.find_all("a")
                        count_links = 0
                        for link in links:
                            if link.get("target") != "_blank":
                                if not args.debug:
                                    count_links += 1
                                    link["target"] = "_blank"
                                    # print(str(link))
                    if args.debug:
                        print('Total Links: ' + str(count_links))
                        print('Total Spans: ' + str(count_spans))
                        print('Total Inline Style Attributes: ' + str(count_inline))
                    # return to start of file and overwrite
                    else:
                        html.seek(0)
                        html.write(str(doc))
                        html.truncate()
