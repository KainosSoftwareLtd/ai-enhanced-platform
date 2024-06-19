import argparse
import os
import csv
from prettytable import PrettyTable
from dotenv import load_dotenv
from azure.identity import EnvironmentCredential
from azure.keyvault.secrets import SecretClient


def main(args):
    load_dotenv()
    try:
        all_secrets = retrieve_all_secrets()
    except Exception as e:
        print(f"Failed to retrieve secrets: {e}")

    # list invdividual secret
    if args.list and args.secret:
        print("Listing key details...")
        try:
            single_secret = retrieve_single_secret(args.secret, all_secrets)
        except Exception as e:
            print(f"Failed to retrieve single secret: {e}")
        if args.value:
            secret_values = retrieve_secret_values(single_secret)
            build_table(single_secret, secret_values)

        else:
            build_table(single_secret, None)

    # disabling individual secret
    if args.disable and args.secret:
        print("Disabling key...")
        try:
            disable_enable_secrets([args.secret], 'Disable')
        except Exception as e:
            print(f"Failed to disable secret {e}")

    # enabling individual secret
    if args.enable and args.secret:
        print("Enabling key")
        try:
            disable_enable_secrets([args.secret], 'Enable')
        except Exception as e:
            print(f"Failed to enable secret {e}")

    # list all keys
    if args.list and args.all:
        print("Listing all secrets...")
        if args.value:
            secret_values = retrieve_secret_values(all_secrets)
            build_table(retrieve_all_secrets(), secret_values)
        else:
            build_table(all_secrets, None)

    # list secrets from provided csv file
    if args.list and args.csv:
        print("Listing secrets from provided csv file...")
        csv_keys = list_csv_keys(retrieve_keys_from_csv(args), all_secrets)
        if args.value:
            secret_values = retrieve_secret_values(csv_keys)
            build_table(csv_keys, secret_values)
        else:
            build_table(csv_keys, None)

    # disable all secerets
    if args.disable and args.all:
        print("Disabling all secrets...")
        try:
            all_secrets_disable = [secret.name for secret in all_secrets]
            disable_enable_secrets(all_secrets_disable, 'Disable')
        except Exception as e:
            print(f"Failed to disable all secrets {e}")

    # enable all secrets
    if args.enable and args.all:
        print("Enabling all secrets...")
        try:
            all_secrets_enable = [secret.name for secret in all_secrets]
            disable_enable_secrets(all_secrets_enable, 'Enable')
        except Exception as e:
            print(f"Failed to enable all secrets {e}")

    # disable secrets from csv
    if args.disable and args.csv:
        print("Disabling secrets from provided csv file...")
        try:
            keys_from_csv = retrieve_keys_from_csv(args)
            disable_enable_secrets(keys_from_csv, 'Disable')
        except Exception as e:
            print(f"Failed to disable secrets from csv {e}")

    # enable secrets from csv
    if args.enable and args.csv:
        print("Enabling secrets from provided csv file...")
        try:
            keys_from_csv = retrieve_keys_from_csv(args)
            disable_enable_secrets(keys_from_csv, 'Enable')
        except Exception as e:
            print(f"Failed to enable secrets from csv {e}")

# retrieve secret values
def retrieve_secret_values(secrets):
    print("Retrieve secret values...")
    vault_client = create_vault_client()
    retrieved_secrets = []
    for secret in secrets:
        retrieved_secrets.append({"key": secret.name, "value": vault_client.get_secret(secret.name).value})
    retrieved_secret_dict = {secret['key']: secret for secret in retrieved_secrets}

    return retrieved_secret_dict

def list_csv_keys(keys, all_secrets):
    print("list csv keys...")
    secret_dict = {secret.name: secret for secret in all_secrets}
    csv_keys = [secret_dict[key] for key in keys if key in secret_dict]

    return csv_keys

# retrieve keys from csv
def retrieve_keys_from_csv(args):
    csv_keys = []
    with open(args.csv, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            csv_keys.append(row[0].strip(','))

    return csv_keys

# Create key vault client
def create_vault_client():
    key_vault_uri = os.environ.get("AZURE_VAULT_ID")
    credential = EnvironmentCredential()
    client = SecretClient(vault_url=key_vault_uri, credential=credential)

    return client

def retrieve_single_secret(key, all_secrets):
    single_secret = [secret for secret in all_secrets if secret.name == key]
    
    return single_secret

# Retrieve all secrets
def retrieve_all_secrets():
    vault_client = create_vault_client()
    secret_properties = vault_client.list_properties_of_secrets()

    return secret_properties

# build table
def build_table(secrets, secret_values):
    table = PrettyTable()
    if secret_values is not None:
        t = PrettyTable(['Key Name', 'Value', 'Enabled', 'Created On', 'Expires On' ])
        for secret in secrets:
            t.add_row([secret.name, secret_values[secret.name]['value'], secret.enabled, secret.created_on, secret.expires_on])
        table = t
    else:
        t = PrettyTable(['Key Name', 'Enabled', 'Created On', 'Expires On'])
        for secret in secrets:
            t.add_row([secret.name, secret.enabled, secret.created_on, secret.expires_on])
        table = t

    print(table)

#  disable all or disable provided list of secrets
def disable_enable_secrets(secret_list, action):
    vault_client = create_vault_client()
    content_type = "text/plain"

    if action == 'Disable':
        for secret in secret_list:
            print(f"Disabling Secret: {secret}")
            vault_client.update_secret_properties(secret, content_type=content_type, enabled=False)
    elif action == 'Enable':
        for secret in secret_list:
            print(f"Enabling Secret: {secret }")
            vault_client.update_secret_properties(secret, content_type=content_type, enabled=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Args for main")
    parser.add_argument('-list', action='store_true', help='Lists all keys within the vault')
    parser.add_argument('-disable', action='store_true', help='Disables all secrets within vault')
    parser.add_argument('-enable', action='store_true', help='Enables all secrets within the vault')
    parser.add_argument('-csv', type=str, required=False, help='Disables all secrets defined in CSV')
    parser.add_argument('-all', action='store_true', required=False, help='Sets the context to all secrets')
    parser.add_argument('-secret', type=str, required=False, help='Provide an individual secret value')
    parser.add_argument('-value', action='store_true', help='Displays the secret value')

    args = parser.parse_args()
    main(args)