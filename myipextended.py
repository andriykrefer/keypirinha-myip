# Keypirinha launcher (keypirinha.com)

import socket

import keypirinha as kp
import keypirinha_net as kpnet
import keypirinha_util as kpu
import time


class MyIpExtended(kp.Plugin):
    """
    Get your public and local IPs directly from Keypirinha.
    """

    def __init__(self):
        super().__init__()
        self._urlopener = kpnet.build_urllib_opener()

    def on_catalog(self):
        self._rebuild_catalog()

    def on_execute(self, item, action):
        kpu.set_clipboard(item.short_desc())
        self._rebuild_catalog()

    def on_events(self, flags):
        if flags & kp.Events.NETOPTIONS:
            self._urlopener = kpnet.build_urllib_opener()
            self._rebuild_catalog()

    def _get_public_ipv4(self):
        try:
            with self._urlopener.open('https://api4.my-ip.io/ip') as res:
                return res.read().decode('utf-8')
        except Exception as ex:
            self.err(ex)
            return 'Could not establish your public ipv4'
    def _get_public_ipv6(self):
        try:
            with self._urlopener.open('https://api6.my-ip.io/ip') as res:
                return res.read().decode('utf-8')
        except Exception as ex:
            self.err(ex)
            return 'Could not establish your public ipv6'

    def _get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        except Exception as ex:
            self.err(ex)
            return 'Could not establish your local ip'

    def _rebuild_catalog(self):
        start_time = time.time()

        public_ipv4 = self._get_public_ipv4()
        public_ipv6 = self._get_public_ipv6()
        local_ip = self._get_local_ip()
        icon=self.load_icon('res://%s/%s'%(self.package_full_name(),'logo.png'))

        catalog = [
            self.create_item(
                category=kp.ItemCategory.KEYWORD,
                label='My IP: Public IPv4',
                short_desc=public_ipv4,
                target='public_ipv4',
                args_hint=kp.ItemArgsHint.FORBIDDEN,
                hit_hint=kp.ItemHitHint.NOARGS,
                icon_handle=icon
            ),
            self.create_item(
                category=kp.ItemCategory.KEYWORD,
                label='My IP: Public IPv6',
                short_desc=public_ipv6,
                target='public_ipv6',
                args_hint=kp.ItemArgsHint.FORBIDDEN,
                hit_hint=kp.ItemHitHint.NOARGS,
                icon_handle=icon
            ),
            self.create_item(
                category=kp.ItemCategory.KEYWORD,
                label='My IP: Local IPv4',
                short_desc=local_ip,
                target='local_ip',
                args_hint=kp.ItemArgsHint.FORBIDDEN,
                hit_hint=kp.ItemHitHint.NOARGS,
                icon_handle=icon
            )
        ]
        self.set_catalog(catalog)

        elapsed = time.time() - start_time
        self.info("Cataloged {} items in {:0.1f} seconds".format(len(catalog), elapsed))
