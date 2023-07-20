import sys

async def leyla_mobile_identify(self):
    payload = {
        'op': self.IDENTIFY,
        'd': {
            'token': self.token,
            'properties': {
                'os': sys.platform,
                'browser': 'Discord Android',
                'device': 'Discord Android',
            },
            'compress': True,
            'large_threshold': 250,
            'v': 3
        }
    }

    await self.call_hooks('before_identify', self.shard_id, initial=self._initial_identify)
    await self.send_as_json(payload)
