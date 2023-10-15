#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from time import sleep

import toml
import requests

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

CONFIG_FILE: Path = Path('config.toml')
LOOP_GUARD: int = 10


def load_toml_file(path: str) -> dict:
    """Load a TOML file and return a dictionary"""
    with open(path, 'r') as f:
        data = toml.load(f)
    return data


class Config:

    def __str__(self):
        return f'Config(api_token={self.api_token}, api_secret={self.api_secret}, update_interval={self.update_interval}, pointers={self.pointers}))'

    def __init__(self):
        pass

    def from_toml(self, path: Path):
        """Load config from TOML file"""
        log.info(f'Loading config from {path.absolute()}..')
        data = load_toml_file(path)

        self.api_token = data['api']['token']
        self.api_secret = data['api']['secret']

        self.update_interval = max(LOOP_GUARD, data['config']['update_interval'])
        self.pointers = data['config']['pointers']


class DomeneshopAPIClient:

    def __init__(self):
        self.secret: str = None
        self.token: str = None
        self.base_url: str = None
        self._base_url: str = None

    def from_config(self, config: Config):
        self.secret = config.api_secret
        self.token = config.api_token
        self.base_url = f'https://XXX:XXX@api.domeneshop.no/v0'
        self._base_url = f'https://{self.token}:{self.secret}@api.domeneshop.no/v0'

    def update_dns_pointer(self, pointer: str, ip: str):
        
        url = f'{self._base_url}/dyndns/update?hostname={pointer}&myip={ip}'
        log.info(f'Updating pointer {pointer} to {ip}, url: {url}')

        r = requests.get(url, timeout=60)

        if r.ok:
            log.info(f'Updated pointer {pointer} to {ip}')
        else:
            log.error(f'Failed to update pointer {pointer} to {ip}: {r.text}')

    def update(self, pointers: list, ip: str):
        for pointer in pointers:
            self.update_dns_pointer(pointer, ip)


class PublicIP:
    def __init__(self):
        pass

    def get(self) -> str:
        public_ip = requests.get('https://api.ipify.org').text
        return public_ip


class EventHandler:
    def __init__(self):
        pass

    def handle(self):
        pass

    def public_ip_changed(self, old: str, new: str, changed: bool):
        pass


def main():
    """DomeneShop Dynamic DNS
    """
    log.info(f'Starting DomeneShop Dynamic DNS updater..')
    config = Config()
    config.from_toml(CONFIG_FILE)
    log.info(f'Loaded config: {config}')

    api_client = DomeneshopAPIClient()
    api_client.from_config(config)

    public_ip = PublicIP()

    sleep_for = int(max(0, config.update_interval - LOOP_GUARD))
    current_public_ip: str = None

    while True:
        sleep(10)
        ip = public_ip.get()
        log.debug(f'Public IP is {ip}')

        if current_public_ip == ip:
            log.debug(f'Public IP has not changed since last check')
        
        else:
            log.info(f'Public IP changed from {current_public_ip} to {ip}')
            current_public_ip = ip
            log.info(f'Updating pointers to new IP..')
            api_client.update(config.pointers, current_public_ip)
        
        if not sleep_for:
            continue
        
        log.info(f'Sleeping for {sleep_for} seconds..')
        sleep(sleep_for)


if __name__ == '__main__':
    main()  