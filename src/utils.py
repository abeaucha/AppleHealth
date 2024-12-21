import os
import pandas as pd
import xml.etree.ElementTree as ElementTree

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
    weight_records = [record.attrib for record in health_root
                      if record.get('type') == record_type]

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


