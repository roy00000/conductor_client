import os
import json

def request_software_packages():
    with open(os.path.join(os.path.dirname(__file__), "../fixtures/sw_packages_no_exact_host.json"), 'r') as data:
        return json.load(data)