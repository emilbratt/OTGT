import importlib


def check_modules(self):
    self.assertIsNotNone(importlib.util.find_spec('aiofiles'))
    self.assertIsNotNone(importlib.util.find_spec('aiohttp'))
    self.assertIsNotNone(importlib.util.find_spec('paho'))
    self.assertIsNotNone(importlib.util.find_spec('streaming_form_data'))
    self.assertIsNotNone(importlib.util.find_spec('uvicorn'))
    self.assertIsNotNone(importlib.util.find_spec('uvloop'))
    self.assertIsNotNone(importlib.util.find_spec('yaml'))
    self.assertIsNotNone(importlib.util.find_spec('matplotlib'))
    self.assertIsNotNone(importlib.util.find_spec('numpy'))
