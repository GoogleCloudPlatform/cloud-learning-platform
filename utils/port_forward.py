import json, os, subprocess
import argparse
from kubernetes import client, config as kubeconfig

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--namespace", "-n")
  parser.add_argument("--redis", action="store_true")
  args = parser.parse_args()
  total = 0
  print(f"Setting up port-forward in namespace '{args.namespace}'")

  port_config_data = []
  with open("./utils/e2e_config.json", "r") as config:
    port_config = json.load(config)
    port_config_data = port_config.get("localPort", [])

  # Let a list of running kubernetes services
  kubeconfig.load_kube_config()
  v1 = client.CoreV1Api()
  serviceList = v1.list_namespaced_service(namespace=args.namespace)
  running = {item.metadata.name for item in serviceList.items}

  for service in port_config_data:
    if service in running:
      port = port_config_data[service]
      cmd = "kubectl port-forward service/%s %s:%s -n %s" % (service, port,
                                                             80, args.namespace)
      print(cmd)
      emulator = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
      total += 1

  # Port forward to redis-master if redis option is enabled
  port = 6379
  service = "redis-master"
  if args.redis:
    cmd = "kubectl port-forward service/%s %s:%s -n %s" % (service, port,
                                                           port, args.namespace)
    print(cmd)
    emulator = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
    total += 1

  print(f"Port-forward configured for {total} services. Use 'pkill -f \"port-forward\"' to terminate")
