import time
import random
import base64
import re
import uuid
import yaml
import os
import json
import requests
from dotenv import load_dotenv
from datetime import date
from secrets import token_bytes
from azure.identity import EnvironmentCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobClient
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2  import PBKDF2HMAC


def main():
    # load .env
    load_dotenv()
    # load key spec
    key_spec = parse_spec()
    # load new manifest file
    manifest = load_manifest()
    # load azure manifest
    az_manifest = load_az_manifest()
    # creating a new manifest by comparing local and azure
    new_manifest = compare_manifests(manifest, az_manifest)
    # pull uuids from az_manifest
    az_uuids = strip_manifest_uuids(az_manifest)
    # retrieved keys 
    retrieved_keys = vault_secret_check(az_uuids)
    # generate new keys
    generated_keys = gen_keys(key_spec, new_manifest)
    # continue to compare safe keys until no duplicates are found
    generated_key_list = None
    while generated_key_list is None:
        if generated_key_list is None:
            generated_key_list = compare_keys(retrieved_keys, generated_keys)
    # push keys to vault
    push_to_vault(generated_key_list)
    # generate and print pwpush urls
    pw_push_urls = get_pwpush_urls(generated_key_list, key_spec)
    # print pwpush_urls
    for url in pw_push_urls:
        print(f"UUID: {url['uuid']}, URL: {url['token']}")
    # update remote manifest
    update_remote_manifest(generated_key_list, az_manifest)


def update_remote_manifest(new_manifest, az_manifest):
    print("Updating remote manifest...")
    uuid_to_user = {az_user['uuid']: az_user for az_user in az_manifest if az_user['uuid']}
    for new_user in new_manifest:
        if new_user['uuid'] in uuid_to_user:
            replace_user = uuid_to_user[new_user['uuid']]
            replace_user_index = az_manifest.index(replace_user)
            new_user.pop('keyvalue')
            az_manifest[replace_user_index] = new_user
        else:
            new_user.pop('keyvalue')
            az_manifest.append(new_user)

    az_manifest = {
        "manifest": {
            "users": az_manifest
        }
    }

    az_manifest = json.dumps(az_manifest).encode('utf-8')
    blob = create_blob_client()
    blob.upload_blob(az_manifest, overwrite=True)


def construct_user_dict(user):
    return {
        "name": user['name'],
        "uuid": user['uuid'], 
        "project": user['project'],
        "contact": user['contact'],
        "keygendate": user['keygendate']
    }


def compare_manifests(local_manifest, az_manifest):
    print("Comparing local and remote manifests")
    new_manifest = []
    az_users_by_uuid = {user['uuid']: user for user in az_manifest}
    for user in local_manifest:
        if user['uuid'] is None:
            new_manifest.append(construct_user_dict(user))
        else: 
            az_user = az_users_by_uuid.get(user['uuid'])
            if az_user:
                if user['regenkey']:
                    new_manifest.append(construct_user_dict(user))
                    print(f"User with UUID: {user['uuid']} has requested a new key...")
                else:
                    print(f"User with UUID: {user['uuid']} exists but has not requested a new key...")

    return new_manifest 


def compare_keys(retrieved_keys, generated_keys):
    safe_keys = []
    for generated_key in generated_keys:
        print(f"Checking key for UUID: {generated_key['uuid']}")
        for retrieved_key in retrieved_keys:
            if generated_key['keyvalue'] == retrieved_key['keyvalue']:
                print(f"Match found against: {generated_key['uuid']} {retrieved_key['uuid']}")
                print("Recycling...")
                return None
        print(f"No matches found against: {generated_key['uuid']}")
        safe_keys.append(generated_key)

    return safe_keys


def load_manifest():
    print("Loading local manifest...")
    manifest_file = open('manifest.json')
    manifest_data = json.load(manifest_file)
    manifest_data = manifest_data['manifest']

    return manifest_data['users']


def load_az_manifest():
    print("Retrieving remote manifest...")
    blob = create_blob_client()
    stream = blob.download_blob() 
    blob_manifest = stream.readall()
    az_manifest_data = json.loads(blob_manifest)
    az_manifest_data = az_manifest_data['manifest']

    return az_manifest_data['users']


def create_blob_client():
    blob = BlobClient(account_url=f"https://{os.environ.get('MANIFEST_STORAGE_ACCOUNT')}.blob.core.windows.net", 
                      container_name=f"{os.environ.get('MANIFEST_CONTAINER_NAME', 'manifest')}",
                      blob_name=f"{os.environ.get('MANIFEST_BLOB_NAME', 'manifest.json')}",
                      credential=f"{os.environ.get('MANIFEST_STORAGE_ACCOUNT_KEY')}")

    return blob


def create_vault_client():
    print("Create Vault Client")
    key_vault_uri = os.environ.get('AZURE_VAULT_ID')
    credential = EnvironmentCredential()
    client = SecretClient(vault_url=key_vault_uri, credential=credential)

    return client


def strip_manifest_uuids(manifest_users):
    print("Obtaining uuids from remote manifest...")
    existing_user_uuids = []
    for user in manifest_users:
        existing_user_uuids.append(user['uuid'])

    return existing_user_uuids

    
def vault_secret_check(uuids):
    print("Retriving existing keys...")
    retrieved_keys = []
    client = create_vault_client()
    for uuid in uuids:
        try:
            retrieved_secret = client.get_secret(uuid)
            retrieved_keys.append({
                "uuid": uuid,
                "keyvalue": retrieved_secret.value
            })
        except ResourceNotFoundError:
            print("Secret Not found")

    return retrieved_keys


def parse_spec():
    print("Reading key spec...")
    with open('key_spec.yml') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)

        return data


def push_to_vault(keys):
    client = create_vault_client()
    for key in keys:
        client.set_secret(key['uuid'], key['keyvalue'])
        print(f"Added Secret {key['uuid']}")


def get_pwpush_urls(keys, key_spec):
    print("Creating pwpush urls...")
    url = "https://pwpush.com/p.json"
    headers = {
        "x-user-email": os.environ.get('PWPUSH_CLIENT', ''),
        "x-user-token": os.environ.get('PWPUSH_TOKEN', '')
    }
    if not headers['x-user-email'] or not headers['x-user-token']:
        print('Error: x-user-email or x-user-token environment variables are not defined')

        return []

    responses = []
    for key in keys:
        data = { 
            "password[payload]": key['keyvalue'],
            "passsword[expire_after_days]": key_spec['PushExpireAfterDays'],
            "password[expire_after_views]": key_spec['PushExpireAfterViews']
        }
        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            responses.append({
                "uuid": key['uuid'], 
                "token" :f"https://pwpush.com/en/p/{json.loads(response.content)['url_token']}"
            })

        except requests.exceptions.RequestException as e:
            print(f"Pwpush request failed: {e}")
            responses.append(None)

    return responses


def gen_keys(key_spec, manifest):
    key_list = []

    for user in manifest:
        current_timestamp = int(time.time())
        seed_value = key_spec['SeedValue']
        salt = token_bytes(16)
        stretch = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    salt=salt,
                    iterations=random.randint(1000,1000),
                    length=key_spec['StretchLength']
        )
        seed = f"{seed_value}{current_timestamp}".encode()
        key_bytes = stretch.derive(seed)
        key_base64 = base64.urlsafe_b64encode(key_bytes).decode()
        api_key = re.sub(r"[^a-zA-Z0-9]", "", key_base64)

        if key_spec['KeyPrefix']:
            api_key = f"{key_spec['KeyPrefix']}-{api_key}"
            if user['uuid'] is None:
                key_obj = {
                "uuid": str(uuid.uuid4()), "keyvalue": api_key,
                "username": user['name'], "keygendate" : date.today().strftime('%Y-%m-%d'),
                "project": user['project'], "contact": user['contact']
                }
                key_list.append(key_obj)
            else:
                key_obj = {
                "uuid": user['uuid'], "keyvalue": api_key,
                "username": user['name'], "keygendate" : date.today().strftime('%Y-%m-%d'),
                "project": user['project'], "contact": user['contact']
                }
                key_list.append(key_obj)
        else:
            if user['uuid'] is None:
                key_obj = {"uuid": str(uuid.uuid4()), "keyvalue": api_key, 
                           "username": user['name'], "keygendate": date.today().strftime('%Y-%m-%d'),
                           "project": user['project'], "contact": user['contact']}
                key_list.append(key_obj)
            else:
                key_obj = {"uuid": user['uuid'], "keyvalue": api_key,  
                           "username": user['name'], "keygendate": date.today().strftime('%Y-%m-%d'), 
                           "project": user['project'], "contact": user['contact']}
                key_list.append(key_obj)

    return key_list

if __name__ == "__main__":
    main()
