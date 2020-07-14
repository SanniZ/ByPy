#!/usr/bin/env python

import csv
import json
import sys
# import io

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')  # set stdout to utf-8

def get_csv_data(path):
    with open(path, 'r', encoding="utf-8") as fd:
        lines = csv.reader(fd)
        result = dict()
        for line in lines:
            line = list(line)
            result[line[0]] = line
        return result
    

def csv2json(data):
    return json.dumps(data)

def json_save(data, path):
    with open(path, 'w', encoding="utf-8") as fd:
        fd.write(data)

if __name__ == '__main__':
    csv_data = get_csv_data('Personal2.csv')
    print("csv-data: ", csv_data)
    dt_data = csv2json(csv_data)
    print("dt_data: ", dt_data.encode())
    js_data = json.dumps(dt_data)
    print("js_data: ", js_data.encode())
    json_save(str(csv_data), 'csv-json.json')