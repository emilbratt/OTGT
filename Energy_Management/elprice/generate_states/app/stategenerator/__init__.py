def stateinit(envar_get: object) -> object:
    api_version = envar_get('STATE_GENERATOR_API_VERSION')

    match api_version:
        case '0':
            from .api0 import State
            return State(envar_get)
