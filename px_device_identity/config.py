"""Configuration"""

import os
import json


def load_json_setup_config(file_path: str = "/etc/config.json"):
    # TODO: Should use module px_install/remote_config.py instead (read_json_config)
    print("Loading registration config from {}".format(file_path))
    config = None
    if os.path.isfile(file_path):
        try:
            file_content = None
            with open(file_path, "r") as reader:
                file_content = reader.read()

            content_dict = json.loads(file_content)

            config = {
                "type": content_dict["type"],
                "timezone": content_dict["timezone"],
                "locale": content_dict["locale"],
                "title": content_dict["title"],
                "location": content_dict["location"],
                "role": content_dict["role"],
                "key_security": content_dict["key_security"],
                "key_type": content_dict["key_type"],
                "domain": content_dict["domain"],
                "host": content_dict["host"],
            }
        except:
            print("Failed to load json registration config from {}".format(file_path))

    return config
