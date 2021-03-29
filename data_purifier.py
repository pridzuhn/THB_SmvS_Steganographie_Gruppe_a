#!/usr/bin/python3
# -*- encoding: utf-8 -*-

# Author: Max Nowak

import csv
import statistics

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


def get_digit_list(input_data):
    data = []
    for i in range(0, int(len(input_data)), 20):
        data.append(input_data[i:i + 20])

    # Aufteilung der Daten in Listen von digits in Gruppen von 20
    all_groups_1_digits = []
    all_groups_2_digits = []
    all_groups_3_digits = []
    for row in data:
        group_1_digit = []
        group_2_digit = []
        group_3_digit = []
        for value in row:
            group_1_digit.append(value[0])
            group_2_digit.append(value[1])
            group_3_digit.append(value[2])
        all_groups_1_digits.append(group_1_digit)
        all_groups_2_digits.append(group_2_digit)
        all_groups_3_digits.append(group_3_digit)

    # alle in int umwandeln
    for i in range(0, len(all_groups_1_digits)):
        all_groups_1_digits[i] = list(all_groups_1_digits[i])
        for j in range(0, len(all_groups_1_digits[i])):
            all_groups_1_digits[i][j] = int(all_groups_1_digits[i][j])

    for i in range(0, len(all_groups_2_digits)):
        all_groups_2_digits[i] = list(all_groups_2_digits[i])
        for j in range(0, len(all_groups_2_digits[i])):
            all_groups_2_digits[i][j] = int(all_groups_2_digits[i][j])

    for i in range(0, len(all_groups_3_digits)):
        all_groups_3_digits[i] = list(all_groups_3_digits[i])
        for j in range(0, len(all_groups_3_digits[i])):
            all_groups_3_digits[i][j] = int(all_groups_3_digits[i][j])

    output = []
    output.append(all_groups_1_digits)
    output.append(all_groups_2_digits)
    output.append(all_groups_3_digits)

    return output


if __name__ == "__main__":
    no_stego_raw_data = __extract_data('NoStego.csv')
    stego_raw_data = __extract_data('Stego_high.csv')

    # data usable for analyisis contains only relevant digits
    no_stego_data = get_sliced_clean_data(no_stego_raw_data, 3, 6)
    stego_data = get_sliced_clean_data(stego_raw_data, 3, 6)

    standard_data = []

    for i in range(0, 100):
        standard_data.append(0)
        standard_data.append(1)
        standard_data.append(2)
        standard_data.append(3)
        standard_data.append(4)
        standard_data.append(5)
        standard_data.append(6)
        standard_data.append(7)
        standard_data.append(8)
        standard_data.append(9)

    print(no_stego_data)
    print(stego_data)

    no_stego_1_digit = []
    no_stego_2_digit = []
    no_stego_3_digit = []

    stego_1_digit = []
    stego_2_digit = []
    stego_3_digit = []

    for value in no_stego_data:
        no_stego_1_digit.append(value[0])
        no_stego_2_digit.append(value[1])
        no_stego_3_digit.append(value[2])

    for value in stego_data:
        stego_1_digit.append(value[0])
        stego_2_digit.append(value[1])
        stego_3_digit.append(value[2])

    no_stego_1_digit = [int(i) for i in no_stego_1_digit]
    no_stego_2_digit = [int(i) for i in no_stego_2_digit]
    no_stego_3_digit = [int(i) for i in no_stego_3_digit]
    stego_1_digit = [int(i) for i in stego_1_digit]
    stego_2_digit = [int(i) for i in stego_2_digit]
    stego_3_digit = [int(i) for i in stego_3_digit]

    no_s_avg_digit_1 = statistics.mean(no_stego_1_digit)
    no_s_avg_digit_2 = statistics.mean(no_stego_2_digit)
    no_s_avg_digit_3 = statistics.mean(no_stego_3_digit)
    s_avg_digit_1 = statistics.mean(stego_1_digit)
    s_avg_digit_2 = statistics.mean(stego_2_digit)
    s_avg_digit_3 = statistics.mean(stego_3_digit)

    no_stego_numbers = [int(i) for i in no_stego_data]
    stego_numbers = [int(i) for i in stego_data]

    no_s_avg_numbers = statistics.mean(no_stego_numbers)
    s_avg_Numbers = statistics.mean(stego_numbers)

    print('\nDurchscnitt aller Zahlen: ')
    print('ns: ' + str(no_s_avg_numbers) + ', s: ' + str(s_avg_Numbers))

    print('\nDurchschnitt aller Stellen: ')
    print('ns: 1: ' + str(no_s_avg_digit_1) + ', 2: ' + str(no_s_avg_digit_2) + ', 3: ' + str(no_s_avg_digit_3))
    print('s: 1: ' + str(s_avg_digit_1) + ', 2: ' + str(s_avg_digit_2) + ', 3: ' + str(s_avg_digit_3))

    # per Digit calculation
    ns_digits_lst = get_digit_list(no_stego_data)

    avg_digits_per_group_ns = []

    for digit in ns_digits_lst:
        avg_per_group = []
        for group in digit:
            avg_per_group.append(statistics.mean(group))
        avg_digits_per_group_ns.append(avg_per_group)

    s_digits_lst = get_digit_list(stego_data)

    avg_digits_per_group_s = []

    for digit in s_digits_lst:
        avg_per_group = []
        for group in digit:
            avg_per_group.append(statistics.mean(group))
        avg_digits_per_group_s.append(avg_per_group)

    print('\nStandard Values:')
    print('standart deviation: ' + str(statistics.stdev(standard_data)))
    print('mean: ' + str(statistics.mean(standard_data)))
    print('median: ' + str(statistics.median(standard_data)))
    print('variance: ' + str(statistics.variance(standard_data)))

    print('\nStandard Deviation in Digits:')

    print('No Steganographie')
    i = 0
    for row in avg_digits_per_group_ns:
        i += 1
        print('Digit ' + str(i) + ': ' + str(statistics.stdev(row)))

    print('Steganographie')
    i = 0
    for row in avg_digits_per_group_s:
        i += 1
        print('Digit ' + str(i) + ': ' + str(statistics.stdev(row)))

    print('\nMean in Digits:')

    print('No Steganographie')
    i = 0
    for row in avg_digits_per_group_ns:
        i += 1
        print('Digit ' + str(i) + ': ' + str(statistics.mean(row)))

    print('Steganographie')
    i = 0
    for row in avg_digits_per_group_s:
        i += 1
        print('Digit ' + str(i) + ': ' + str(statistics.mean(row)))

    print('\nMedian in Digits:')

    print('No Steganographie')
    i = 0
    for row in avg_digits_per_group_ns:
        i += 1
        print('Digit ' + str(i) + ': ' + str(statistics.median(row)))

    print('Steganographie')
    i = 0
    for row in avg_digits_per_group_s:
        i += 1
        print('Digit ' + str(i) + ': ' + str(statistics.median(row)))

    print('\nVariance in Digits:')

    print('No Steganographie')
    i = 0
    for row in avg_digits_per_group_ns:
        i += 1
        print('Digit ' + str(i) + ': ' + str(statistics.variance(row)))

    print('Steganographie')
    i = 0
    for row in avg_digits_per_group_s:
        i += 1
        print('Digit ' + str(i) + ': ' + str(statistics.variance(row)))

    print(ns_digits_lst)

    step_size = 20

    no_s_group_avg = []
    for i in range(0, len(no_stego_data), step_size):
        group = []
        for j in range(0, step_size):
            try:
                group.append(no_stego_numbers[i + j])
            except:
                break
        no_s_group_avg.append(statistics.mean(group))

    s_group_avg = []
    for i in range(0, len(no_stego_data), step_size):
        group = []
        for j in range(0, step_size):
            try:
                group.append(stego_numbers[i + j])
            except:
                break
        s_group_avg.append(statistics.mean(group))

    # print('\nDurchschnitt nach Gruppen\n')
    # for i in range(0, len(no_s_group_avg) - 1):
    #     print('Gruppe: ' + str(i) + ' ns: ' + str(no_s_group_avg[i]) + ', s: ' + str(s_group_avg[i]))
