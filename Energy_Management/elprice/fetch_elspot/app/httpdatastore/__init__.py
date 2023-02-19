# based on the value found in envar HTTPDATASTORE_API_VERSION
# this imports the class Handle() from that specific
# script and returns it

def httpdatastoreinit(envar_get: object) -> object:
   '''
      calling this function will return selected object by envars
   '''
   API_VERSION = envar_get('HTTPDATASTORE_API_VERSION')

   match API_VERSION:
      case '0':
         from .api0 import Handle
         return Handle(envar_get)

      case '1':
         from .api1 import Handle
         return Handle(envar_get)

      case None:
         print('Error: missing envar')
         print('..set an api page via envar HTTPDATASTORE_API_VERSION')

      case _:
         print('Error: invalid envar:', API_VERSION)

   print('namespace:', __name__)
   print('script:', __file__)
   exit(1)
