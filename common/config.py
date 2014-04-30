import json

class Config:

    def __init__(self, config_file):
        self.config_file = config_file

    def get_value_for(self, key):
        """ Get the config value for a key
        """
        # the file is opened each time in case some content has been added recently
        fp = open(self.config_file, "r")
        json_data = json.load(fp)
        fp.close()
        try:
            return json_data["config"][key]
        except:
            return None



if __name__ == "__main__":
    c = Config("config_sample.json")
    print c.get_value_for("key1")
    print c.get_value_for("key2")
    print c.get_value_for("key3")
        
