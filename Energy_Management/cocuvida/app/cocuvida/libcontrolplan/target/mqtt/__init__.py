from .target import TargetMQTT


# simple publish function that can be called without instanciating the target
async def publish(target_entry: dict, state_value: str) -> bool:
    raise Exception('MethodNotImplemented')
