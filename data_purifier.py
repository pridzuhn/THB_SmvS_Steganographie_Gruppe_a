#!/usr/bin/python3
# -*- encoding: utf-8 -*-

# Author: Max Nowak

import csv


def __extract_data(filename):
    """Input: filename - name of CSV file from which to extract data
    Output: extracted data - List of all enties, containing all Information from csv"""
    __file = open(filename, newline='')
    __reader = csv.reader(__file, delimiter=' ')

    __extracted_data = []

    for row in __reader:
        __extracted_data.append(row)
    return tuple(__extracted_data)


def __filter_responses(__data):
    """Input: extracted data - List of all enties, containing all Information from csv
    Output: filtered data - List of all responses, containing only entries starting with 66"""
    __filtered_data = []

    for row in __data:
        if '66' in row[0]:
            __filtered_data.append(row)

    return tuple(__filtered_data)


def __clean_micro_seconds(__data):
    """Input: filtered data - List of all responses, containing only entries starting with 66
    Output: clean data - List of all microsecond values"""
    __data_micro_sec = []

    for row in __data:
        __data_micro_sec.append(row[3].split(sep='.')[1])

    return tuple(__data_micro_sec)


def get_clean_data(__raw_data):
    """Input: extracted data - List of all enties, containing all Information from csv
    Output: clean data - list of all microsecond values"""
    __filtered_data = __filter_responses(__raw_data)
    __clean_data = __clean_micro_seconds(__filtered_data)

    return tuple(__clean_data)


def __slice_data(__data, start, end):
    """Input: clean Data - list of all microsecond values
    Output: sliced data - list of all entries sliced to [start:end)"""
    __sliced_data = []

    for row in __data:
        __sliced_data.append(row[start:end])

    return tuple(__sliced_data)


def get_sliced_clean_data(__raw_data, start, end):
    """Input: extracted data - List of all enties, containing all Information from csv
        Output: sliced data - list of all entries sliced to [start:end)"""
    return tuple(__slice_data(get_clean_data(__raw_data), start, end))


def extract_clean_data(filename):
    """Input: filename - name of CSV file from which to extract data
    Output: clean Data - list of all microsecond values"""
    return get_clean_data(__extract_data(filename))


def extract_sliced_clean_data(filename):
    """Input: filename - name of CSV file from which to extract data
    Output: clean Data - list of all microsecond values"""
    return get_sliced_clean_data(__extract_data(filename), 3, 6)


if __name__ == "__main__":
    no_stego_raw_data = __extract_data('NoStego.csv')
    stego_raw_data = __extract_data('Stego_high.csv')

    # data usable for analyisis contains only relevant digits
    no_stego_data = get_sliced_clean_data(no_stego_raw_data, 3, 6)
    stego_data = get_sliced_clean_data(stego_raw_data, 3, 6)

    print(no_stego_data)
    print(stego_data)
