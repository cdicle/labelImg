import argparse
import json
import os

def listjson(path):
    """Lists json in a given folder."""
    return [fn for fn in os.listdir(path) if os.path.splitext(fn)[1] == '.json']

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Converts Pascal VOC type multiple annotation to SSTK type \
            single annotation file')
    parser.add_argument('--input_folder', required=True,
                        help='path to input folder for Pascal VOC type annotations')
    parser.add_argument('--output_file', required=True,
                        help='path to output file for SSTK type annotations')

    args = parser.parse_args()
    input_folder = args.input_folder
    output_file = args.output_file

    sstk_annotations = {}
    for json_name in listjson(input_folder):
        print(json_name)
        with open(os.path.join(input_folder, json_name)) as fp:
            voc_annotation = json.load(fp)

        def convert(voc):
            p1, p2, p3, p4 = voc['points']
            x1, y1 = p1
            x2, y2 = p3
            sstk={}
            sstk['bbox'] = [x1, y1, x2, y2]
            sstk['label'] = voc['label']

            return sstk

        sstk_annotation = [convert(item) for item in voc_annotation]
        image_name = os.path.splitext(json_name)[0] + '.jpg'
        sstk_annotations[image_name] = sstk_annotation

        with open(output_file, 'w') as fp:
            json.dump(sstk_annotations, fp)
