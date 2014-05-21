# -*- coding: utf-8 -*-

import json

class Security:

    def __init__(self, security_file):
        self.security_file = security_file

    def is_granted(self, id):
        """ Check if the id is authorized or not
        """
        # the file is opened each time in case some content has been added recently
        fp = open(self.security_file, "r")
        json_data = json.load(fp)
        fp.close()
        if id in json_data['granted']:
            return True
        return False



if __name__ == "__main__":
    s = Security("security_sample.json")
    print s.is_granted("azertyui")
    print s.is_granted("xxxrtyui")
        
