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
        self.devices = {}

    async def load_target_entry(self, target_entry: dict) -> None:
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
            shelly_info = await aioshelly_get_info(self.aiohttp_session, host)
            if 'gen' in shelly_info:
                gen = shelly_info.get('gen') # 2nd generation shelly devices broadcast their generation
            else:
                gen = 1 # 1st generation shelly devices do not broadcast their generation
            options = ConnectionOptions(host, user, pwd)
            try:
                if gen == 1:
                    device = await BlockDevice.create(self.aiohttp_session, coap_context, options, init)
                elif gen == 2:
                    device = await RpcDevice.create(self.aiohttp_session, ws_context, options, init)
                else:
                    raise ShellyError("Unknown Gen")
            except FirmwareUnsupported as err:
                print(f"Device firmware not supported, error: {repr(err)}")
                return
            except InvalidAuthError as err:
                print(f"Invalid or missing authorization, error: {repr(err)}")
                return
            except DeviceConnectionError as err:
                print(f"Error connecting to {options.ip_address}, error: {repr(err)}")
                return
            self.devices[alias] = {}
            self.devices[alias]['gen'] = gen
            self.devices[alias]['relay_id'] = relay_id
            self.devices[alias]['device'] = device

    async def publish_state(self, alias: str, state: str) -> bool:
        relay = self.devices[alias]['relay_id']

        # just use http for now
        if self.devices[alias]['gen'] == 1:
            path = f'relay/{relay}'
            params = {'turn': state}
            await self.devices[alias]['device'].http_request('get', path, params)
            return True

        elif self.devices[alias]['gen'] == 2:
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
            await self.devices[alias]['device'].call_rpc('post', params)
            return True

        return False
