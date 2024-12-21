import os
import pandas as pd
import xml.etree.ElementTree as ElementTree

def parse_weight_records(input_file, outdir = 'data/', prefix = 'AppleHealth'):

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


def parse_dietary_record(input_file, record_type, outdir = 'data/', prefix = 'AppleHealth'):

    if 'Dietary' not in record_type:
        raise Exception("Not an Apple Health dietary record: {}".format(record_type))

    # Parse Apple Health data and get root of the XML file
    health_root = ElementTree.parse(input_file).getroot()

    # Create a list of the dietary records
    records = []
    for element in health_root.iter('Record'):
        if element.get('type') == record_type:
            element_dict = element.attrib.copy()
            element_dict.update({element[0].get('key'):element[0].get('value')})
            records.append(element_dict)

    # Get the dictionary keys
    records_keys = list(records[0].keys())

    # TODO: This is breaking because of entries from DrinkControl app
    # Reshape the dictionary
    records_dict = {key:None for key in records_keys}
    for key in records_dict.keys():
        records_dict[key] = [record[key] for record in records]

    for i in range(len(records)):
        print(i)
        records[i]['meal']

    # Export the dietary data to CSV
    outfile = record_type.replace('HKQuantityTypeIdentifier', '')
    outfile = '_'.join([prefix, outfile])
    outfile = outfile + '.csv'
    outfile = os.path.join(outdir, outfile)
    pd.DataFrame(records_dict).to_csv(outfile, index = False)

    return outfile


def parse_dietary_records(input_file, outdir = 'data/', prefix = 'AppleHealth'):

    # Parse Apple Health data and get root of the XML file
    health_root = ElementTree.parse(input_file).getroot()

    dietary_types = [record.get('type') for record in health_root.iter('Record')]
    dietary_types = sorted(list(set(dietary_types)))
    dietary_types = [record for record in dietary_types if 'Dietary' in record]

    outfiles = []
    # for dietary_type in dietary_types[:5]:
    dietary_type = 'HKQuantityTypeIdentifierDietaryEnergyConsumed'
    outfile = parse_dietary_record(input_file, record_type = dietary_type, outdir = outdir, prefix = prefix)
    outfiles.append(outfile)

    return outfiles