#LISTS
names = ["Harry", "Ron", "Hermione", "Ginny"]
print(names)
names.append("Draco")
print(names)
print(len(names[0]), len(names[1]))
names.sort()
print(names)

#TUPLES
coordinateX = 10.0
coordinateY = 20.0
coordinateZ = 30.0
coordinate = (10.0, 20.0, 30.0)
print(coordinate)

#SETS
#CREATE
s = set()
t = set()

#ADD ELEMENTS
s.add(1)
s.add(2)
s.add(3)
s.add(4)
s.remove(2)
print(s)