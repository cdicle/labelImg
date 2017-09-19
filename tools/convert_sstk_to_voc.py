import argparse
import json
import os


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Converts SSTK type single annotation file to Pascal VOC \
        type multiple files')
    parser.add_argument('--input_file', required=True,
                        help='path to input for SSTK type annotation file')
    parser.add_argument('--output_folder', required=True,
                        help='path to output folder for Pascal VOC type annotations')

    args = parser.parse_args()
    input_file = args.input_file
    output_folder = args.output_folder

    with open(input_file) as fp:
        annotations = json.load(fp)

    for image_name in annotations.keys():
        print('Converting ' + image_name)

        def convert(sstk):
            x1, y1, x2, y2 = sstk['bbox']
            voc={}
            voc['label']='face'
            voc['points']=[[x1,y1],[x2,y1],[x2,y2],[x1,y2]]
            voc['line_color']=None
            voc['fill_color']=None
            voc['difficult']=False
            return voc

        sstk_annotation=annotations[image_name]
        voc_annotation=[convert(item) for item in sstk_annotation]

        json_name = os.path.splitext(image_name)[0] + '.json'
        with open(os.path.join(output_folder, json_name), 'w') as fp:
            json.dump(voc_annotation, fp)
