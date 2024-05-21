import xml.etree.ElementTree as ET

# Parse the XML file
tree = ET.parse('getCurrentTrainsXML.xml')
root = tree.getroot()

# Define the namespace used in the XML
namespace = {'ns': 'http://api.irishrail.ie/realtime/'}

# Find all TrainCode elements and print their text content
for train_code in root.findall('.//ns:TrainCode', namespace):
    print(train_code.text)
