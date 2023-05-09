import asyncio

from cocuvida.libcontrolplan.target.mqtt import TargetMQTT


async def publish_state(target_entry: dict):
    '''
        target_entry for mqtt
        {
            include_entry: bool
            username: <user>
            password: <password>
            host: <host>
            port: <port>
            client_id: <client_id>
            keep_alive: <seconds>
            tls: bool/string
            will: null/string
            transport: 'tcp'
            states:
                test:
                    qos: <0, 1 or 2>
                    retain: bool
                    message: '<string>'
                some_other_state:
                    qos: <0, 1 or 2>
                    retain: bool
                    message: '<string>'
                ....
            entries:
                topic_a: some/topic
                topic_b: some/other/topic
                ..
        }

        will try to publish the state in "test" for all topics in "entries"
    '''
    if not target_entry['include_entry']:
        return True

    target_obj = TargetMQTT()
    await target_obj.load_target_entry(target_entry)
    publish_tasks = []
    for alias in target_entry['entries']:
        task = target_obj.publish_state(alias, 'test')
        publish_tasks.append(task)

    results = await asyncio.gather(*publish_tasks, return_exceptions=True)
    for result in results:
        continue

    return True
