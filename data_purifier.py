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


def rolling_detect(data, window_size):
    """Input: sliced data - list of all entries sliced to [start:end), size of window
        function iteraties through given data"""
    count_digits = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    total = 0

    fA = False

    s_live_list_digits = []

    for row in data:
        for value in row:
            s_live_list_digits.append(value)

    print(s_live_list_digits)

    for value in s_live_list_digits:
        value = int(value)
        if value == 0:
            count_digits[0] += 1
        if value == 1:
            count_digits[1] += 1
        if value == 2:
            count_digits[2] += 1
        if value == 3:
            count_digits[3] += 1
        if value == 4:
            count_digits[4] += 1
        if value == 5:
            count_digits[5] += 1
        if value == 6:
            count_digits[6] += 1
        if value == 7:
            count_digits[7] += 1
        if value == 8:
            count_digits[8] += 1
        if value == 9:
            count_digits[9] += 1

        # reduce attempts, cutoff low amounts of Data to reduce false positives
        if int(value) % int(window_size) == 0 and total > 50:

            removed_outlier_first_grade = []

            data_std = statistics.stdev(count_digits)
            data_mean = statistics.mean(count_digits)

            # clean std and mean of simple outliers because of small samplesize
            for outlier in count_digits:
                if outlier > data_mean + data_std:
                    pass
                else:
                    removed_outlier_first_grade.append(outlier)

            clean_data_std = statistics.stdev(removed_outlier_first_grade)
            clean_data_mean = statistics.mean(removed_outlier_first_grade)

            # there is an anomaly with 0, so i had to increase it ti 7 usually should work with 3*
            cutoff = clean_data_std * 7
            upper_limit = clean_data_mean + cutoff
            lower_limit = clean_data_mean - cutoff

            for outlier in count_digits:
                if outlier > upper_limit or outlier < lower_limit:
                    fA = True
                    print("\nAnomaly detected")
                    print(outlier)
                    print(count_digits)
                    print("Limits:")
                    print(upper_limit)
                    print(lower_limit)
                    print("std: " + str(clean_data_std))
                    print("mean: " + str(clean_data_mean))

        total += 1
    return fA


def extra_info_overall(stego_data, no_stego_data):
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


if __name__ == "__main__":
    no_stego_raw_data = __extract_data('NoStego.csv')
    stego_raw_data = __extract_data('Stego_high.csv')

    # data usable for analyisis contains only relevant digits
    # data with 66 rows
    # no_stego_data = __slice_data(__clean_micro_seconds(no_stego_raw_data), 0, 6)
    # stego_data = __slice_data(__clean_micro_seconds(stego_raw_data), 3, 6)

    # data with all positions
    # no_stego_data = __clean_micro_seconds(__filter_responses(no_stego_raw_data))
    # stego_data = __clean_micro_seconds(__filter_responses(stego_raw_data))

    # data without 66 rows
    no_stego_data = get_sliced_clean_data(no_stego_raw_data, 3, 6)
    stego_data = get_sliced_clean_data(stego_raw_data, 3, 6)

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

    s_digits_lst = get_digit_list(stego_data)
    ns_digits_lst = get_digit_list(no_stego_data)

    # Digits Totals/ Percentage
    # No Stego
    count_digits = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    total = 0
    for row in ns_digits_lst:
        for group in row:
            for value in group:
                total += 1
                if value == 0:
                    count_digits[0] += 1
                if value == 1:
                    count_digits[1] += 1
                if value == 2:
                    count_digits[2] += 1
                if value == 3:
                    count_digits[3] += 1
                if value == 4:
                    count_digits[4] += 1
                if value == 5:
                    count_digits[5] += 1
                if value == 6:
                    count_digits[6] += 1
                if value == 7:
                    count_digits[7] += 1
                if value == 8:
                    count_digits[8] += 1
                if value == 9:
                    count_digits[9] += 1
            # print(count_digits)

    print('\nNo Steganographie')
    print('\nTotal Values: ')
    for i in range(0, len(count_digits)):
        print(str(i) + ': ' + str(count_digits[i]))

    print('\nPercentage: ')
    for i in range(0, len(count_digits)):
        print(str(i) + ': ' + str((count_digits[i] / total) * 100))

    # Stego
    count_digits = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    total = 0
    for row in s_digits_lst:
        for group in row:
            for value in group:
                total += 1
                if value == 0:
                    count_digits[0] += 1
                if value == 1:
                    count_digits[1] += 1
                if value == 2:
                    count_digits[2] += 1
                if value == 3:
                    count_digits[3] += 1
                if value == 4:
                    count_digits[4] += 1
                if value == 5:
                    count_digits[5] += 1
                if value == 6:
                    count_digits[6] += 1
                if value == 7:
                    count_digits[7] += 1
                if value == 8:
                    count_digits[8] += 1
                if value == 9:
                    count_digits[9] += 1
            # print(count_digits)

    print('\nSteganographie')
    print('\nTotal Values: ')
    for i in range(0, len(count_digits)):
        print(str(i) + ': ' + str(count_digits[i]))

    print('\nPercentage: ')
    for i in range(0, len(count_digits)):
        print(str(i) + ': ' + str((count_digits[i] / total) * 100))

    step_size = 20

    print('\nDetect Anomaly in No Steganographie Data:')
    anomaly_found = rolling_detect(no_stego_data, 20)
    if anomaly_found:
        print("Anomaly Found in No Stego")
    else:
        print("No Anomaly Found in No Stego")

    print('\nDetect Anomaly in Steganographie Data:')
    anomaly_found = rolling_detect(stego_data, 20)
    if anomaly_found:
        print("Anomaly Found in Stego")
    else:
        print("No Anomaly Found in Stego")


class LiveDetector:
    count_digits = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    total = 0

    def check_anomaly(self):
        """Checks for all given Data if an anomaly was found
        :return False No Anomaly
        :return True Anomaly found
        print details to cmd"""
        removed_outlier_first_grade = []
        found_Anomaly = False

        data_std = statistics.stdev(self.count_digits)
        data_mean = statistics.mean(self.count_digits)

        # clean std and mean of simple outliers because of small samplesize
        for outlier in self.count_digits:
            if outlier > data_mean + data_std:
                pass
            else:
                removed_outlier_first_grade.append(outlier)

        clean_data_std = statistics.stdev(removed_outlier_first_grade)
        clean_data_mean = statistics.mean(removed_outlier_first_grade)

        # there is an anomaly with 0, so i had to increase it ti 7 usually should work with 3*
        cutoff = clean_data_std * 7
        upper_limit = clean_data_mean + cutoff
        lower_limit = clean_data_mean - cutoff

        for outlier in self.count_digits:
            if outlier > upper_limit or outlier < lower_limit:
                found_Anomaly = True
                print("\nAnomaly detected")
                print(outlier)
                print(count_digits)
                print("Limits:")
                print(upper_limit)
                print(lower_limit)
                print("std: " + str(clean_data_std))
                print("mean: " + str(clean_data_mean))

        return found_Anomaly

    def add_data(self, clean_sliced_data):
        s_live_list_digits = []

        for __row in clean_sliced_data:
            for __value in row:
                s_live_list_digits.append(__value)

        for __value in s_live_list_digits:
            __value = int(__value)
            if value == 0:
                self.count_digits[0] += 1
            if value == 1:
                self.count_digits[1] += 1
            if value == 2:
                self.count_digits[2] += 1
            if value == 3:
                self.count_digits[3] += 1
            if value == 4:
                self.count_digits[4] += 1
            if value == 5:
                self.count_digits[5] += 1
            if value == 6:
                self.count_digits[6] += 1
            if value == 7:
                self.count_digits[7] += 1
            if value == 8:
                self.count_digits[8] += 1
            if value == 9:
                self.count_digits[9] += 1
