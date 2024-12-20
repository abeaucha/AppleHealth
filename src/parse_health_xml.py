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
import sys
import pandas as pd
import xml.etree.ElementTree as ElementTree


# Environment ----------------------------------------------------------------

BASEDIR = '/Users/Antoine/Documents/Health/AppleHealthDashboard/'


# Modules --------------------------------------------------------------------

def extract_data_export(file = 'export.zip', outdir = 'data/'):

    """
    Extract Apple Health export from ZIP file.
    :return:
    """

    print("Extracting Apple Health data...")

    # Check if export exists in Downloads
    # Move to data directory if True
    downloads = '/Users/Antoine/Downloads/'
    if os.path.exists(os.path.join(downloads, file)):
        os.rename(os.path.join(downloads, file),
                  os.path.join(outdir, file))

    # File path
    file = os.path.join(outdir, file)

    # Extract Apple Health export
    subprocess.run(['unzip', '-f', file, '-d', outdir])

    # Path to export XML file
    export_xml = os.path.join(outdir, 'apple_health_export', 'export.xml')

    return export_xml


def parse_weight_data(input_file, outdir = 'data/', prefix = 'AppleHealth'):

    """

    :param input_file:
    :param outdir:
    :param prefix:
    :return:
    """

    print("Building Apple Health weight data...")

    # Record type for weight data
    record_type = 'HKQuantityTypeIdentifierBodyMass'

    # Parse Apple Health data and get root of the XML file
    health_root = ElementTree.parse(input_file).getroot()

    # Get all weight records
    weight_records = [child.attrib for child in health_root if child.get('type') == record_type]

    # Get the attribute keys for the weight records
    weight_keys = list(weight_records[0].keys())

    # Re-organize the records dictionary
    weight_dict = {key: None for key in weight_keys}
    for key in weight_dict.keys():
        weight_dict[key] = [record[key] for record in weight_records]

    # Export the weight data to CSV
    outfile = record_type.replace('HKQuantityTypeIdentifier', '')
    outfile = '_'.join([prefix, outfile])
    outfile = outfile + '.csv'
    outfile = os.path.join(outdir, outfile)
    pd.DataFrame(weight_dict).to_csv(outfile, index = False)

    return outfile


def main():

    """

    :return:
    """


    # Output directory
    output_dir = os.path.join(BASEDIR, 'data')

    # Prefix to output files
    output_prefix = 'AppleHealth'

    # Extract Apple Health export
    xml_file = extract_data_export(outdir = output_dir)

    # Build weight data CSV
    weight_file = parse_weight_data(input_file = xml_file,
                                    outdir = output_dir,
                                    prefix = output_prefix)

    # record_types_all = [node.get('type') for node in health_root.iter('Record')]

    # dietary_records = [record for record in ]
    # dietary_types = [record for record in record_types_unique if 'Dietary' in record]
    # dietary_types

    return


# Main -----------------------------------------------------------------------
if __name__ == '__main__':
    main()