import os

class ConfigReader:
    @staticmethod
    def read_config(file_path="config.txt"):
        config_data = {}
        if not os.path.exists(file_path):
            return config_data
        
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    if '=' in line:
                        key, value = line.split('=', 1)
                        config_data[key.strip()] = value.strip()
        except Exception as e:
            print(f"Error reading config: {e}")
            
        return config_data

    @staticmethod
    def get_db_config():
        config = ConfigReader.read_config()
        return {
            'host': config.get('Primary DB Server Ip', '127.0.0.1'),
            'port': int(config.get('Primary DB Server Port', '3306')),
            'database': config.get('DB Name', ''),
            'user': config.get('DB User Id', 'root'),
            'password': config.get('DB User Pwd', '')
        }
