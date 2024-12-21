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

import utils

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
    weight_file = utils.parse_weight_data(input_file = xml_file,
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
