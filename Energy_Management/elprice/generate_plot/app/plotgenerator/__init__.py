def plotinit(envar_get: object) -> object:
    api_version = envar_get('PLOT_GENERATOR_API_VERSION')

    match api_version:
        case '0':
            from .api0 import Plot
            return Plot(envar_get)
