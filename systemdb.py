import xml.etree.ElementTree as ET
import os
from argparse import ArgumentParser


def getSerialFromJennyDB(filename="JennyDB.xml"):
    if not os.path.isfile(filename):
        return False
    else:
        tree = ET.parse(filename)
        root = tree.getroot()
        if root.tag == "PQDCDatabase":
            # print(root.attrib)
            for item in root.iter("Device"):
                if item.attrib["Name"] == "System":
                    return f"{item.attrib['Serial']}"
            return False
        else:
            return False


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("filename", help="JennyDB", type=str, nargs="?", default="./")
    args = parser.parse_args()
    if not os.path.isfile(args.filename):
        filename = "JennyDB.xml"
    serial = getSerialFromJennyDB()
    if serial:
        print(f"Lumninosa Serial number: {serial}")
    else:
        print(f"error reading the serial number from {filename}")
