import asyncio
import yaml

from cocuvida.controlplanparser import ControlplanParser
from cocuvida.controlplanparser.sections.target.shelly import Entry as ShellyEntry


class ControlplanTargets:

    def __init__(self):
        f = open('tests/test_data/example_controlplan.yaml')
        self.controlplan = yaml.safe_load(f.read())
        self.cpparser = ControlplanParser()
        f.close()

    def publish_states_to_shelly_target(self):
        asyncio.run(self.cpparser.load_controlplan(self.controlplan))
        shelly = ShellyEntry(self.controlplan['target']['shelly'])
        asyncio.run(shelly.publish_state('off'))
        return True
