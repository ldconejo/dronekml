'''
Processes drone location data
'''
# pylint: disable=C0301

import csv
import re

import argparse
import simplekml

def process_csv(filename):
    """
    Processes csv file
    """
    tag_dictionary = {}
    pattern = re.compile(r'numTags: (\d+)')
    tag_pattern = re.compile(r'TAG\d+')
    with open(filename) as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            result = pattern.findall(row[0])
            if result:
                if int(result[0]) > 0:
                    date_time = row[1]
                    latitude = row[2]
                    longitude = row[3]
                continue
            result = tag_pattern.findall(row[8])
            if result:
                tag_name = row[8]
                signal_strength = row[9]
                dict_entry = {
                    "latitude": latitude,
                    "longitude": longitude,
                    "date_time": date_time,
                    "signal_strength": signal_strength
                }
                #print(f"Tag {tag_name} at latitude {latitude}, longitude {longitude} on {date_time} with a strength of {signal_strength}")
                tag_dictionary[tag_name] = dict_entry
    print(tag_dictionary)
    return tag_dictionary

def create_kml(tag_dictionary, output_file):
    '''
    Created a new KML file from a list of geo tags
    '''
    kml = simplekml.Kml()

    for tag, value in tag_dictionary.items():
        longitude = value["longitude"]
        latitude = value["latitude"]
        date_time = value["date_time"]
        signal_strength = value["signal_strength"]
        kml.newpoint(
            name=tag,
            coords=[(longitude, latitude)],
            description=f"{tag}\nDate: {date_time}\nLatitude: {latitude}\nLongitude: {longitude}\nSignal strenght: {signal_strength}"
            )
    kml.save(output_file)

if __name__ == '__main__':
    # Setup script arguments
    parser = argparse.ArgumentParser(description='Converts csv-formatted drone data to a KML map file.')
    parser.add_argument('-i', '--input', help='Input csv file', required=True)
    parser.add_argument('-o', '--output', help='Input csv file', default='output.kml')
    args = parser.parse_args()
    create_kml(process_csv(args.input), args.output)
