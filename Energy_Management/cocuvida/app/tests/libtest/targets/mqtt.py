from cocuvida.libcontrolplan.target.mqtt import TargetMQTT

from .const import MQTT_TEST_STATE


async def publish_state(target_entry: dict):
    '''
        target_entry for mqtt
        {
            include_entry: bool
            topic: '<mqtt/topic/string>'
            entries:
                key1: '<message_string>',
                key2: '<message_string>',
                ...
        }

        with topic in "topic"
            ..try to publish the message in MQTT_TEST_STATE
            ..try to publish messages found in "entries",
    '''
    if not target_entry['include_entry']:
        return True
    return True
