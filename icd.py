import xml.etree.ElementTree as ET

class icd():
    def __init__(self):
        super(icd, self).__init__()
        self.icd = ET.parse('MessageXMLStructure.xml')
        self.root = self.icd.getroot()
        self.get_number_of_Income_messages = 0;
        self.get_number_of_outcome_messages = 0;

    def get_number_of_headers(self):
        return len(self.root[0])
    def get_number_of_Income_messages(self):
        return self.get_number_of_Income_messages

    def get_number_of_Income_messages(self):
        return self.get_number_of_outcome_messages



    def read_headers(self):
        headers = []
        for header in self.icd.iter('header'):
            for element,j in zip(header,range(len(header))):
                headers.append(element.get('name'))
        return headers

    def read_income_messages(self):
        message = []
        for child in self.icd.iter('income'):
            for grandchild in child:
                    for element, j in zip(grandchild, range(len(grandchild))):
                        message.append(element.tag)
        self.get_number_of_Income_messages = len(message)
        return message

    def read_outcome_messages(self):
        message = []
        for child in self.icd.iter('outcome'):
            for grandchild in child:
                    for element, j in zip(grandchild, range(len(grandchild))):
                        message.append(element.tag)
        self.get_number_of_outcome_messages = len(message)
        return message





