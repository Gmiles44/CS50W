class Flight():
    def __init__(self, capacity):
        self.capacity = capacity
        self.passengers = []

    def open_seats(self):
        return self.capacity - len(self.passengers)
    
    def add_passenger(self, name):
        if not self.open_seats():
            return False            
        self.passengers.append(name)
        return True

flight = Flight(3)
people = ["Harry", "Ron", "Hermione", "Ginny"]
for person in people:
    success = flight.add_passenger(person)
    if success:
        print(f"Added {person} to flight")
    else:
        print(f"No seats available for {person}")