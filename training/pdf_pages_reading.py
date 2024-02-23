# https://stackoverflow.com/questions/51567750/extract-specific-pages-of-pdf-and-save-it-with-python
# information = [(filename1,startpage1,endpage1), (filename2, startpage2, endpage2), ...,(filename19,startpage19,endpage19)].
import argparse
import shlex
import sys

import concurrent.futures
import json
from PyPDF2 import PdfReader


def pdf_extract(pdf: str, segments: str):
    """
    pdf: str
    segments: start,end
    """
    segments = segments.split(',')
    start_page, end_page = int(segments[0]), int(segments[1])
    context_keeper = []

    with open(pdf, 'rb') as read_stream:
        pdf_reader = PdfReader(read_stream)

        for page_number in range(end_page - start_page + 1):
            page = pdf_reader.pages[start_page + page_number]

            # extracting text from page
            text = page.extract_text()
            context_keeper.append(
                {
                    "context": text
                }
            )

    with open('data/context.json', 'w') as file:
        json.dump(context_keeper, file)

def __pdf_extract(pair):
    return pdf_extract(*pair)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--args", nargs=2, action="append")
    all_args = parser.parse_args(shlex.split(" ".join(sys.argv[1:])))

    kwargs = {}
    if all_args.args:
        kwargs = {arg[0]: arg[1] for arg in all_args.args}

    # Single
    pdf_extract(**kwargs)
