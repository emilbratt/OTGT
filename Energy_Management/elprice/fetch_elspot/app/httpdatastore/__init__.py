# based on the value found in envar WEB_DATASTORE_API_VERSION
# this imports the class Handle() from that specific
# script and returns it

def httpdatastoreinit(envar_get: object) -> object:
   '''
      calling this function will return selected object by envars
   '''
   API_VERSION = envar_get('WEB_DATASTORE_API_VERSION')

   match API_VERSION:
      case '0':
         from .api0 import Handle
         return Handle(envar_get)

      case 'test':
         from .test import Handle
         return Handle()

      case None:
         print('Error: set an api page via envar WEB_DATASTORE_API_VERSION')
         print('..then re-run script')

      case _:
         print('Error: envar WEB_DATASTORE_API_VERSION is set to:', API_VERSION)
         print('this is not a valid page')

   # if function did not return any value, we have an error (see above)
   print('namespace:', __name__+ '.Handle()')
   print('script:', __file__)
   exit(1)
