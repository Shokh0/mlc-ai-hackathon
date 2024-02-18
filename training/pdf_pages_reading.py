# https://stackoverflow.com/questions/51567750/extract-specific-pages-of-pdf-and-save-it-with-python
# information = [(filename1,startpage1,endpage1), (filename2, startpage2, endpage2), ...,(filename19,startpage19,endpage19)].

import concurrent.futures
from multiprocessing import freeze_support
from pathlib import Path

from PyPDF2 import PdfWriter, PdfReader


def pdf_extract(pdf, segments, together=False):
    """
    pdf: str | Path
    segments: [(start, end), {'start': int, 'end': int}]
    """
    pdf_writer = PdfWriter()
    with open(pdf, 'rb') as read_stream:
        pdf_reader = PdfReader(read_stream)
        pdf_writer_segment = PdfWriter()
        for segment in segments:
            # support {'start': 3, 'end': 3} or (start, end)
            try:
                start_page, end_page = segment['start'], segment['end']
            except TypeError:
                start_page, end_page = segment
            for page_num in range(start_page - 1, end_page):
                if together:
                    pdf_writer.add_page(pdf_reader.pages[page_num])
                else:
                    pdf_writer_segment.add_page(pdf_reader.pages[page_num])
            p = Path(pdf)
            if not together:
                ouput = p.parent / p.with_stem(f'{p.stem}_pages_{start_page}-{end_page}')
                with open(ouput, 'wb') as out:
                    pdf_writer_segment.write(out)
    if together:
        ouput = p.parent / p.with_stem(f'{p.stem}_extracted')
        with open(ouput, 'wb') as out:
            pdf_writer.write(out)


def __pdf_extract(pair):
    return pdf_extract(*pair)


def pdf_extract_batch(pdfs, workers=20):
    """
    pdfs = {pdf_name: [(1, 1), ...], ...}
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(__pdf_extract, pdfs.items())


if __name__ == '__main__':
    freeze_support()
    pdf_name = r"C:\Users\sente\Desktop\AI-Hackathon\mlc-ai-hackathon\HackathonRules.pdf"
    segments = [(1, 1)]
    # Single

    pdf_extract(pdf_name, segments)
    # Batched (Concurrent)

    # pdfs = {pdf_name: segments}
    # pdf_extract_batch(pdfs)
