"""This script allows you to extract and export all the secrets found in a kubernetes namespace in json format."""


import os
import json
import subprocess
import logging
import base64
import argparse

logging.basicConfig(encoding='utf-8', level=logging.INFO)
SECRETS_PATH = os.path.join(os.getcwd(), "secrets")

def get_secrets_without_label_helm(namespace: str = ""):
    if namespace:
        filter_namespace = ['-n', namespace]
    else:
        filter_namespace = ['--all-namespaces']

    command = [
        "kubectl",
        "get",
        "secrets",
        *filter_namespace,
        "-o=jsonpath={range .items[*]}{.metadata.name}{''}{.metadata.labels.owner}{'\\n'}{end}"
    ]
    logging.debug(f'command {command}')

    try:
        result = subprocess.run(command, check=True,
                                capture_output=True, text=True)
        secrets = result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running kubectl: {e}")
        return []

    # Filter out secrets that don't have the tag 'owner=helm'
    filtered_secrets = [{"name": secret, "namespace": namespace}
                        for secret in secrets.split('\n') if 'helm' not in secret and secret]
    return filtered_secrets


def write_secret_to_file(secret, decoded_secrets):
    _file = os.path.join(SECRETS_PATH, secret["namespace"], secret["name"])
    # Ensure the directory exists
    os.makedirs(os.path.dirname(_file), exist_ok=True)
    with open(f'{_file}.json', 'w') as secret_file:
        json.dump(decoded_secrets, secret_file, indent=4)


def get_secret_data(secret):
    command = [
        "kubectl",
        "get",
        "secrets",
        secret["name"],
        "-n",
        secret["namespace"],
        "-o=jsonpath={.data}"
    ]
    logging.debug(f'command {command}')
    try:
        result = subprocess.run(command, check=True,
                                capture_output=True, text=True)
        secrets_data = result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running kubectl: {e}")
        return []

    try:
        data = json.loads(secrets_data)
    except json.decoder.JSONDecodeError:
        logging.error('The string does NOT contain valid JSON')
        return

    decoded_secrets = {k.lower(): base64.b64decode(v).decode('utf-8')
                       for k, v in data.items()}
    write_secret_to_file(secret, decoded_secrets)


if __name__ == "__main__":
    namespaces = []
    parser = argparse.ArgumentParser(description="Export to json file k8s secrets")
    parser.add_argument('-n', 
                        '--namespaces', 
                        type=str, 
                        nargs='+', 
                        dest='namespaces',
                        default="")

    args = parser.parse_args()
    namespaces = args.namespaces
    for namespace in namespaces:
        secrets = get_secrets_without_label_helm(namespace)
        for secret in secrets:
            get_secret_data(secret)
            logging.info(f' from: {secret["namespace"]} - create: {secret["name"]} ')

    logging.info(f'You can see all secrets expoered on  {SECRETS_PATH}')