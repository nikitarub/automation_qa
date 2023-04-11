from common import log
from common.fs import Fs
from common.explain import explain
import json


def update_version_file(filename, data):
    with open(filename, 'w') as f:
        f.write(json.dumps(data))


def read_version_file(filename, version_key):
    with open(filename, 'r') as f:
        version_json = json.loads(f.read())
        version_str = version_json[version_key]
        if not (version_str.count('.') == 2):
            error_msg = f"Version {version_str} is not supported. Must be SemVer."
            log.error(error_msg)
            raise RuntimeError(error_msg)
        major, minor, patch = version_str.split('.')
        return version_json, major, minor, patch


def update_version(version, version_file, version_key = "version"):
    log.info(f"Updating version: {version}")
    version_res = "0.0.0"
    major, minor, patch = version_res.split(".")
    version_json = {}
    version_json, major, minor, patch = explain(
        "Will read version file",
        what_to_return=[{'version': '0.0.0'}, '0', '0', '0']
        )(read_version_file)(version_file, version_key)
    if version == 'patch':
        patch = int(patch) + 1
        version_res = f"{major}.{minor}.{patch}"
        log.info(f"Version patched: {version_res}")
    elif version == 'minor':
        minor = int(minor) + 1
        version_res = f"{major}.{minor}.{patch}"
        log.info(f"Version minor updated: {version_res}")
    elif version == 'major':
        major = int(major) + 1
        version_res = f"{major}.{minor}.{patch}"
        log.info(f"Version major updated: {version_res}")
    elif version.count('.') == 2:
        version_res = version
        log.info(f"Version updated to: {version}")
    else:
        error_msg = f"Unknown version: {version}. It must be one of [major|minor|patch] or in 'x.x.x' format, eg. SemVer!"
        log.error(error_msg)
        raise RuntimeError(error_msg)
    log.info(f"Updating to version in file...")
    version_json[version_key] = version_res
    explain("Version file will be updated")(update_version_file)(version_file, version_json)
    log.info("Versioning file has been updated.")
    
    