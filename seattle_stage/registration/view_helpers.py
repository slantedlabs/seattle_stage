## Object Form Pair
#
#  Takes an object with a .formInitialData() member function and returns a
#  pair of that object and a form object of the type FormClass as initialized
#  with the object's initial form data.
#
def objectFormPair(obj, FormClass):
  return (obj, FormClass(obj.formInitialData()))

