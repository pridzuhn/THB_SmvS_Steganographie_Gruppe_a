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
    # Die Liste von allen Reihen wird aufgeteilt in 20 Werte lange Blöcke
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
    """Input: sliced data - list of all entries sliced to [start:end), size of window in rows
        function iteraties through given data"""
    count_digits = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    total = 0

    fA = False

    s_live_list_digits = []

    # data ist eine Liste aller relevanten Werte in cronologischer Reihenfolge {604,244,951,394, ... }
    # s_live_list_digits zerlegt diese Liste in eine Liste einelner Ziffern in cronologischer Reihenfolge

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

        # zählt jeden einzelnen Wert in der Liste und fügt ihm entsprechend der Ziffer den gezählten hinzu

        # reduce attempts, cutoff low amounts of Data to reduce false positives
        # windows_size * 3 da jede Reihe aus 3 Ziffern besteht
        if total % int(window_size * 3) == 0 and total > 50:

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


def test_detection(data, window_size, cutoff_mult):
    """Input: sliced data - list of all entries sliced to [start:end), size of window in rows, multiplicator to trigger alarm
        function iteraties through given data"""
    count_digits = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    tested_values = 1
    result_lst = []
    total_windows = 0

    s_live_list_digits = []

    # data ist eine Liste aller relevanten Werte in cronologischer Reihenfolge {604,244,951,394, ... }
    # s_live_list_digits zerlegt diese Liste in eine Liste einelner Ziffern in cronologischer Reihenfolge

    for row in data:
        for value in row:
            s_live_list_digits.append(value)

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

        # zählt jeden einzelnen Wert in der Liste und fügt ihm entsprechend der Ziffer den gezählten hinzu

        # reduce attempts, cutoff low amounts of Data to reduce false positives
        if tested_values % int(
                window_size * 3) == 0:  # -"total > 50" um test des eigentlichen detectierens zu ermöglichen

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
            cutoff = clean_data_std * cutoff_mult
            upper_limit = clean_data_mean + cutoff
            lower_limit = clean_data_mean - cutoff

            fa = False
            for outlier in count_digits:
                if outlier > upper_limit or outlier < lower_limit:
                    fa = True
            if fa:
                result_lst.append([total_windows, True])
            else:
                result_lst.append([total_windows, False])

            total_windows += 1
            count_digits = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        tested_values += 1

    return result_lst


def calc_performance(result_no_stego, result_stego):
    ns_total_wind = len(result_no_stego)
    s_total_wind = len(result_stego)

    ns_pos = 0
    for row in result_no_stego:
        if row[1]:
            ns_pos += 1

    s_pos = 0
    for row in result_stego:
        if row[1]:
            s_pos += 1
    # gesamte windows, anz true negatives, anz false positives, % true negatives, % false positives
    # gesamte windows, anz true positives, anz false negatives, % true positives, % false negatives
    return {
        "total_windows": ns_total_wind,
        "TruePos": s_pos,
        "FalsePos": ns_pos,
        "TrueNegatives": ns_total_wind - ns_pos,
        "FalseNegatives": s_total_wind - s_pos,
        "ProzentTruePos": s_pos / s_total_wind,
        "ProzentFalsePos": ns_pos / ns_total_wind,
        "ProzentTrueNegatives": (ns_total_wind - ns_pos) / ns_total_wind,
        "ProzentFalseNegatives": (s_total_wind - s_pos) / s_total_wind,
    }


def performance_test(stego_data, no_stego_data):
    window_size = 20
    cutoff_mult = 7

    print("\nPlease enter the windows size (standard = 20): ")
    window_size = int(input())

    print("\nPlease enter the cutoff multiplicator (standard = 7): ")
    cutoff_mult = int(input())

    print("\n\nDetected Anomalies per Window: ")
    print("No Stego:")
    result_no_stego = test_detection(no_stego_data, window_size, cutoff_mult)
    for row in result_no_stego:
        print(str(row[0]) + ': ' + str(row[1]))

    print("\nStego:")
    result_stego = test_detection(stego_data, window_size, cutoff_mult)
    for row in result_stego:
        print(str(row[0]) + ': ' + str(row[1]))

    performance = calc_performance(result_no_stego, result_stego)

    # gesamte windows, anz true negatives, anz false positives, % true negatives, % false positives
    # gesamte windows, anz true positives, anz false negatives, % true positives, % false negatives

    # "total_windows": ns_total_wind,
    # "TruePos": s_pos,
    # "FalsePos": ns_pos,
    # "TrueNegatives": ns_total_wind - ns_pos,
    # "FalseNegatives": s_total_wind - s_pos,
    # "ProzentTruePos": s_pos / s_total_wind,
    # "ProzentFalsePos": ns_pos / ns_total_wind,
    # "ProzentTrueNegatives": (ns_total_wind - ns_pos) / ns_total_wind,
    # "ProzentFalseNegatives": (s_total_wind - s_pos) / s_total_wind,

    print('\nPerformance:')
    print('Tests overall: ' + str(performance["total_windows"]))
    print('True Positives: ' + str(performance["TruePos"]))
    print('False Positives: ' + str(performance["FalsePos"]))
    print('True Negatives: ' + str(performance["TrueNegatives"]))
    print('False Negatives: ' + str(performance["FalseNegatives"]))
    print('Prozentual True Positives: ' + str(performance["ProzentTruePos"]) + " %")
    print('Prozentual False Positives: ' + str(performance["ProzentFalsePos"]) + " %")
    print('Prozentual True Negatives: ' + str(performance["ProzentTrueNegatives"]) + " %")
    print('Prozentual False Negatives: ' + str(performance["ProzentFalseNegatives"]) + " %")


def check_distribution(stego_data, no_stego_data):
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

    # ns_digits_lst sind Listen die aus 3 Listen bestehen
    # jede Liste enthält respektive die erste, zweite und dritte stelle der Zahlen in cronologischer reihenfolge
    # jede Liste ist in 20 Wertegruppen unterteilt

    # s_digits_lst =[
    # [ [4, 2, 9, 9, 9, 8, 9, 4, 5, 4, 8, 4, 9, 1, 8, 9, 6, 4, 4, 1], [5, 4, 5, 3, 4, 8, 0, 9, 2, 4, 9, 9, 6, 4, 5, 4, 9, 4, 7, 9], [5, 5, 9, 6, 4, 9, 4, 3, 4, 7, 4, 9, 2, 6, 9, 2, 1, 4, 9, 9], ... ]
    # [ [0, 4, 5, 9, 9, 5, 7, 9, 3, 7, 4, 8, 0, 9, 7, 3, 9, 2, 7, 4], [4, 7, 4, 3, 8, 4, 2, 4, 9, 7, 4, 9, 1, 7, 4, 6, 0, 9, 1, 6], [9, 3, 9, 9, 6, 4, 9, 6, 5, 4, 1, 4, 9, 9, 4, 9, 9, 8, 4, 4], ... ]
    # [ [4, 4, 4, 4, 1, 9, 5, 1, 9, 7, 9, 4, 2, 8, 9, 2, 4, 9, 2, 3], [4, 6, 4, 4, 2, 8, 4, 2, 6, 9, 8, 3, 9, 9, 5, 4, 0, 3, 9, 6], [4, 9, 5, 7, 9, 9, 7, 9, 9, 7, 4, 9, 5, 9, 6, 2, 9, 2, 3, 4], ... ]
    # ]
    # s_digits_lst[0][0][0] = 4
    # s_digits_lst[1][0][0] = 0
    # s_digits_lst[2][0][0] = 4
    # bilden zusammen die 3 Ziffern der ersten Zahl in korrekter Rheinfolge
    # s_digits_lst[0][0][1] = 2
    # s_digits_lst[1][0][1] = 4
    # s_digits_lst[2][0][1] = 4
    # bilden zusammen die 3 Ziffern der zweiten Zahl in korrekter Rheinfolge
    # s_digits_lst[0][0][0] = 5
    # s_digits_lst[1][0][0] = 4
    # s_digits_lst[2][0][0] = 4
    # bilden zusammen die 3 Ziffern der 21 Zahl in korrekter Rheinfolge

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


if __name__ == "__main__":
    # data usable for analyisis contains only relevant digits
    # data with 66 rows
    # no_stego_data = __slice_data(__clean_micro_seconds(no_stego_raw_data), 0, 6)
    # stego_data = __slice_data(__clean_micro_seconds(stego_raw_data), 3, 6)

    # data with all positions
    # no_stego_data = __clean_micro_seconds(__filter_responses(no_stego_raw_data))
    # stego_data = __clean_micro_seconds(__filter_responses(stego_raw_data))

    # data without 66 rows

    no_stego_raw_data = __extract_data('NoStego.csv')
    stego_raw_data = __extract_data('Stego_high.csv')

    no_stego_data = get_sliced_clean_data(no_stego_raw_data, 3, 6)
    stego_data = get_sliced_clean_data(stego_raw_data, 3, 6)

    performance_test(stego_data, no_stego_data)

    # print('\nDetect Anomaly in No Steganographie Data:')
    # anomaly_found = rolling_detect(no_stego_data, 20)
    # if anomaly_found:
    #     print("Anomaly Found in No Stego")
    # else:
    #     print("No Anomaly Found in No Stego")
    #
    # print('\nDetect Anomaly in Steganographie Data:')
    # anomaly_found = rolling_detect(stego_data, 20)
    # if anomaly_found:
    #     print("Anomaly Found in Stego")
    # else:
    #     print("No Anomaly Found in Stego")

    # check_distribution(stego_data, no_stego_data)

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
                print(self.count_digits)
                print("Limits:")
                print(upper_limit)
                print(lower_limit)
                print("std: " + str(clean_data_std))
                print("mean: " + str(clean_data_mean))

        return found_Anomaly

    def add_data(self, clean_sliced_data):
        s_live_list_digits = []

        for __row in clean_sliced_data:
            for __value in __row:
                s_live_list_digits.append(__value)

        for __value in s_live_list_digits:
            __value = int(__value)
            if __value == 0:
                self.count_digits[0] += 1
            if __value == 1:
                self.count_digits[1] += 1
            if __value == 2:
                self.count_digits[2] += 1
            if __value == 3:
                self.count_digits[3] += 1
            if __value == 4:
                self.count_digits[4] += 1
            if __value == 5:
                self.count_digits[5] += 1
            if __value == 6:
                self.count_digits[6] += 1
            if __value == 7:
                self.count_digits[7] += 1
            if __value == 8:
                self.count_digits[8] += 1
            if __value == 9:
                self.count_digits[9] += 1
