import xml.etree.ElementTree as ET
import os
import sys

if __name__ == "__main__":
    xmls_path = "xml"
    target_path = "txt"

    for xmlFilePath in os.listdir(xmls_path):
        print(os.path.join(xmls_path, xmlFilePath))
        try:
            tree = ET.parse(os.path.join(xmls_path, xmlFilePath))

            root = tree.getroot()
        except Exception as e:  
            print("parse test.xml fail!")
            sys.exit()
        f = open(target_path + "/" + os.path.splitext(xmlFilePath)[0] + ".txt", 'w')
        for bndbox in root.iter('bndbox'):
            node = []
            for child in bndbox:
                node.append(int(child.text))
            x1, y1 = node[0], node[1]
            x3, y3 = node[2], node[3]
            x2 ,y2 = x3 ,y1
            x4, y4 = x1, y3
            string = '' + str(x1) + ',' + str(y1) + ',' +str(x2)+',' +str(y2)+',' + str(x3) + ',' + str(y3)+','+str(x4)+','+str(y4);
            f.write(string + '\n')

        f.close()
