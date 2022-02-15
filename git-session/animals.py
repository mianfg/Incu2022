import sys

class Animal(object):
  def __init__(self, name, age):
    self.name = name
    self.age = age
    
  def speak(self):
    print("I am", self.name, "and I am", self.age, "years old")
    
class Dog(Animal):
  def __init__(self, name, age):
    super().__init_(name, age)
    self.type = 'dog'
    
  def speak(self):
    super().speak()
    print("Woof!")

class Cat(Animal):
  def __init__(self, name, age):
    super().__init_(name, age)
    self.type = 'cat'
    
  def speak(self):
    super().speak()
    print("Meow!")

if __name__ == "__main__":
  if len(sys.args) < 3:
    raise Exception("Too few arguments")
  if sys.argv[3] == 'dog':
    called_animal = Dog(sys.args[1], sys.args[2])
  if sys.argv[3] == 'cat':
    called_animal = Cat(sys.args[1], sys.args[2])
  called_animal.speak()
