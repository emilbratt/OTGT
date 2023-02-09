def mqttpublishinit(envar_get: object) -> object:

    api_version = envar_get('MQTT_PUBLISH_API_VERSION')

    match api_version:
        case '0':
            from .api0 import Publish
        case _:
            print('Error:')
            print('envar MQTT_PUBLISH_API_VERSION is invalid, currenclty set to:', api_version)
            exit(1)

    return Publish(envar_get)
