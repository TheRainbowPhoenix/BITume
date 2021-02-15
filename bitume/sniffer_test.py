# coding: utf-8
import csv

import os

import pandas as pd

from tabulator import Stream

import mimetypes

# Common delimiters
delimiters = [',', ';', '|', ':', '/', '-', '.']
codepages = ('latin1', 'iso-8859-1', 'cp1252', 'cp850', 'utf-8')


def sniff_csv(file: str):
    mime, encoding = mimetypes.guess_type(file)
    print(mime, encoding)

    file_size = os.path.getsize(file)
    print(file_size)


    with open(file, 'rb') as f:
        chunk = f.read(1024)

        decoded = False
        codepage = None
        block = ''
        delimiter = None
        for cp in codepages:
            try:
                block = chunk.decode(cp)
                codepage = cp
                decoded = True
                break
            except UnicodeDecodeError:
                pass
        if decoded:
            try:
                dialect = csv.Sniffer().sniff(block)
                f.seek(0)
                delimiter = dialect.delimiter
                print(dialect.delimiter)

                # reader = csv.reader(f, dialect)
                print('DECODED LINE ' + codepage)
            except Exception as e:
                print("### Could not determine delimiter")
            print(file)

        blob = None
        if mime is not None:
            if 'excel' in mime:
                try:
                    blob = pd.read_excel(f)
                except Exception as e:
                    print(e)
            elif 'tab-separated-values' in mime:
                delimiter = '\t'
                try:
                    blob = pd.read_csv(f, encoding=codepage, delimiter=delimiter)
                except Exception as e:
                    print(e)

                    for cp in codepages:
                        try:
                            blob = pd.read_csv(f, encoding=cp, delimiter=delimiter)
                        except Exception:
                            pass
            elif 'csv' in mime:
                try:
                    if delimiter is not None:
                        try:
                            blob = pd.read_csv(f, encoding=codepage, delimiter=delimiter)
                        except Exception as e:
                            print(e)

                            for cp in codepages:
                                try:
                                    blob = pd.read_csv(f, encoding=cp, delimiter=delimiter)
                                except Exception:
                                    pass
                    else:
                        for delim in delimiters:
                            try:
                                blob = pd.read_csv(f, encoding=codepage, delimiter=delim)
                                break
                            except Exception as e:
                                print(e)
                except Exception as e:
                    print(e)
            elif 'html' in mime:
                try:
                    blob = pd.read_html(f)
                except Exception as e:
                    print(e)
        else:
            if decoded and delimiter is not None:
                try:
                    blob = pd.read_csv(f, encoding=codepage, delimiter=delimiter)
                except Exception as e:
                    print(e)

                    for cp in codepages:
                        try:
                            blob = pd.read_csv(f, encoding=cp, delimiter=delimiter)
                        except Exception:
                            pass

        if blob is None:
            if (
                    file.lower().endswith('.xls') or
                    file.lower().endswith('.xlsx') or
                    file.lower().endswith('.xlsm') or
                    file.lower().endswith('.xlsb') or
                    file.lower().endswith('.odf') or
                    file.lower().endswith('.ods') or
                    file.lower().endswith('.odt')
            ):
                if file_size > 500_000:
                    print("### WARNING, HUGE FILE CAN SLOW YOUR PC DOWN")
                else:
                    try:
                        blob = pd.read_excel(f, sheet_name=None)
                    except Exception as e:
                        print(e)
        if blob is None:
            print("###\n### BLOB IS NONE\n###")
        else:
            print(blob)

        # use 'line'

    # with open(file, encoding = 'cp850') as f:
    #     chunk = f.read(1024)
    #     dialect = csv.Sniffer().sniff(chunk)
    #     f.seek(0)
    #     reader = csv.reader(f, dialect)
    #
    #     print(dialect.delimiter)
    #
    #     line_count = 0
    #     for cols in reader:
    #         if line_count == 4:
    #             break
    #
    #         print(cols)
    #         line_count += 1

    # with Stream(folder + file, headers=1) as stream:
    #     print(stream.headers)  # [header1, header2, ..]
    #
    #     line_count = 0
    #
    #     for row in stream:
    #         if line_count == 4:
    #             break
    #         print(row)  # [value1, value2, ..]
    #         line_count += 1


if __name__ == '__main__':
    for folder in [
        'samples/data/'
        # 'samples/messy/',
        # 'samples/jburkardt-fsu-edu/',
    ]:
        for file in os.listdir(folder):
            sniff_csv(folder + file)
