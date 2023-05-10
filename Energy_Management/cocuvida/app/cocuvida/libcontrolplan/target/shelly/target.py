import aiohttp

from aioshelly.block_device import COAP, BlockDevice
from aioshelly.common import ConnectionOptions
from aioshelly.common import get_info as aioshelly_get_info
from aioshelly.const import WS_API_URL
from aioshelly.exceptions import (
    DeviceConnectionError,
    FirmwareUnsupported,
    InvalidAuthError,
    ShellyError,
)
from aioshelly.rpc_device import RpcDevice, WsServer

from .const import COAP_PORT, WS_PORT


class TargetShelly:
    def __init__(self, aiohttp_session: aiohttp.ClientSession):
        self.aiohttp_session = aiohttp_session
        self.entries = {}

    async def load_target_entry(self, target_entry: dict) -> bool:
        init = True
        coap_context = COAP()
        await coap_context.initialize(COAP_PORT)
        ws_context = WsServer()
        await ws_context.initialize(WS_PORT, WS_API_URL)
        user = target_entry['user']
        pwd = target_entry['password']
        for alias, entry in target_entry['entries'].items():
            host = entry[0]
            relay_id = entry[1]
            options = ConnectionOptions(host, user, pwd)
            try:
                shelly_info = await aioshelly_get_info(self.aiohttp_session, host)
                if 'gen' in shelly_info:
                    gen = shelly_info.get('gen') # 2nd generation shelly devices broadcast their generation
                else:
                    gen = 1 # 1st generation shelly devices do not broadcast their generation
                if gen == 1:
                    device = await BlockDevice.create(self.aiohttp_session, coap_context, options, init)
                elif gen == 2:
                    device = await RpcDevice.create(self.aiohttp_session, ws_context, options, init)
            except FirmwareUnsupported as err:
                print(f'Error: Device firmware not supported, {repr(err)}')
                return False
            except InvalidAuthError as err:
                print(f'Error: Invalid or missing authorization, {repr(err)}')
                return False
            except DeviceConnectionError as err:
                print(f'Error: host {options.ip_address}, {repr(err)}')
                return False
            self.entries[alias] = {}
            self.entries[alias]['gen'] = gen
            self.entries[alias]['relay_id'] = relay_id
            self.entries[alias]['device'] = device
        return True

    async def publish_state(self, alias: str, state: str) -> bool:
        relay = self.entries[alias]['relay_id']

        # just use http for now
        if self.entries[alias]['gen'] == 1:
            path = f'relay/{relay}'
            params = {'turn': state}
            await self.entries[alias]['device'].http_request('get', path, params)
            return True

        elif self.entries[alias]['gen'] == 2:
            params = { 'params': {"id": relay} }
            match state:
                case 'toggle':
                    params['method'] = 'Switch.Toggle'
                case 'on':
                    params['method'] = 'Switch.Set'
                    params['params']['on'] = True
                case 'off':
                    params['method'] = 'Switch.Set'
                    params['params']['on'] = False
            await self.entries[alias]['device'].call_rpc('post', params)
            return True

        return False
