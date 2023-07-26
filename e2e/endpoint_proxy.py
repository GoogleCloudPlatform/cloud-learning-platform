import json, os


port_config_data = []
port_config_path = os.path.join(os.getcwd(), "e2e/e2e_config.json")

with open(port_config_path, "r") as config:
  port_config = json.load(config)
  port_config_data = port_config.get("localPort", [])


def get_baseurl(service_name):
  local_port = port_config_data[service_name]
  return "http://localhost:%s" % (local_port)
