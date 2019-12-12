from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Dict
import csv
import pandas as pd

csv_file = 'pascal.csv'
csv_header = ['filename','class','xmin','ymin','xmax','ymax']
with open(csv_file, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_header)
    writer.writeheader()

dict_data = {}


class XMLHandler:
    def __init__(self, xml_path: str or Path):
        self.xml_path = Path(xml_path)
        self.root = self.__open()

    def __open(self):
        with self.xml_path.open() as opened_xml_file:
            self.tree = ET.parse(opened_xml_file)
            return self.tree.getroot()

    def return_boxes_class_as_dict(self) -> Dict[int, Dict]:
        """
        Returns Dict with class name and bounding boxes.
        Key number is box number

        :return:
        """

        boxes_dict = {}
        for index, sg_box in enumerate(self.root.iter('object')):
            boxes_dict[index] = {"name": sg_box.find("name").text,
                                 "xmin": int(sg_box.find("bndbox").find("xmin").text),
                                 "ymin": int(sg_box.find("bndbox").find("ymin").text),
                                 "xmax": int(sg_box.find("bndbox").find("xmax").text),
                                 "ymax": int(sg_box.find("bndbox").find("ymax").text)}

        return boxes_dict


def converter(xml_files: str, output_folder: str) -> None:
    """
    Function converts pascal voc formatted files into ODM-File format

    :param xml_files: Path to folder with xml files
    :param output_folder: Path where results files should be written
    :return:
    """
    xml_files = sorted(list(Path(xml_files).rglob("*.xml")))


    for xml_index, xml in enumerate(xml_files, start=1):
        
        filename = f"{xml_index:09}.txt"
        filename_path = Path(output_folder) / filename
        xml_content = XMLHandler(xml)
        boxes = xml_content.return_boxes_class_as_dict()
        
        for each in boxes:
            # print(boxes[each]['name'])
            try:
                if (boxes[each]['name']) == 'car':
                    dict_data['filename'] = xml
                    
                    dict_data['class'] = boxes[each]['name']

                    dict_data['xmin'] = boxes[each]['xmin']
                    dict_data['ymin'] = boxes[each]['ymin']
                    dict_data['xmax'] = boxes[each]['xmax']
                    dict_data['ymax'] = boxes[each]['ymax']
                    with open(csv_file, 'a') as csvfile:
                        writer = csv.DictWriter(csvfile,fieldnames=csv_header)
                        writer.writerow(dict_data)


                    print(xml,boxes[each])
            except:
                continue


    #     with open(filename_path, "a") as file:
    #         for box_index in boxes:
    #             box = boxes[box_index]
    #             box_content = f"{box['name']} {box['xmin']} {box['ymin']} {box['xmax']} {box['ymax']}\n"
    #             file.write(box_content)

    # print(f"Converted {len(xml_files)} files!")

    
if __name__ == '__main__':
    XML_FOLDER = "./VOCdevkit/VOC2012/Annotations/"
    OUTPUT_FOLDER =  "./hi/"

    converter(XML_FOLDER, OUTPUT_FOLDER)

