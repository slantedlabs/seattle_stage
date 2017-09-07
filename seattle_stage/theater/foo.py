def dec(cls):
  print(getattr(cls, "_decorated_function", cls).__name__.lower())
  print("{}".format(cls.__name__.lower()))
  cls.class_method()
  return cls


@dec
class Foo:
  @classmethod
  def class_method(cls):
    print("hello, world")

f = Foo()
