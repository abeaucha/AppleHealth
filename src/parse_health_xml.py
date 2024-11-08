#!/usr/bin/env python3
# ----------------------------------------------------------------------------
# parse_health_xml.py 
# Author: Antoine Beauchamp
# Created: September 10th, 2024

"""
Description
-----------

"""

# Packages -------------------------------------------------------------------

import os
import subprocess
import pandas as pd
import xml.etree.ElementTree as ET


# Modules --------------------------------------------------------------------

# def extract_data_export():
#     return
#
# def parse_weight_data():
#     return
#
# def main():
#     return

# Main -----------------------------------------------------------------------

if __name__ == '__main__':

    # Base directory
    base_dir = '/Users/Antoine/Documents/Health/AppleHealth/'

    # Data directory
    data_dir = 'data/'

    # Apple Health data export
    apple_export = 'export.zip'
    apple_export = os.path.join(data_dir, apple_export)

    # Extract Apple Health export
    subprocess.run(['unzip', '-f', apple_export, '-d', data_dir])
    # subprocess.run(['unzip', apple_export, '-d', data_dir])

    # Input and output directories
    input_dir = os.path.join(data_dir, 'apple_health_export')
    output_dir = data_dir

    # Prepend base directory
    input_dir = os.path.join(base_dir, input_dir)
    output_dir = os.path.join(base_dir, output_dir)

    # Create output directory if needed
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Prefix to output files
    output_prefix = 'AppleHealth'

    # Input file containing Apple Health data
    input_file = 'export.xml'
    input_file = os.path.join(input_dir, input_file)

    # Parse Apple Health data
    health = ET.parse(input_file)

    # Get the root of the XML file
    health_root = health.getroot()

    # Record type for weight data    
    record_type = 'HKQuantityTypeIdentifierBodyMass'

    # Get all weight records
    weight_records = [child.attrib for child in health_root 
                      if child.get('type') == record_type]

    # Get the attribute keys for the weight records
    weight_keys = list(weight_records[0].keys())

    # Re-organize the records dictionary
    weight_dict = {key: None for key in weight_keys}
    for key in weight_dict.keys():
        weight_dict[key] = [record[key] for record in weight_records]

    # Export the weight data to CSV
    outfile = record_type.replace('HKQuantityTypeIdentifier', '')
    outfile = '_'.join([output_prefix, outfile])
    outfile = outfile+'.csv'
    outfile = os.path.join(output_dir, outfile)
    pd.DataFrame(weight_dict).to_csv(outfile, index = False)

    record_types_all = [node.get('type') for node in health_root.iter('Record')]

    # dietary_records = [record for record in ]
    # dietary_types = [record for record in record_types_unique if 'Dietary' in record]
    # dietary_types