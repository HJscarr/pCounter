class Pub:
    def __init__(self, name, location, total_capacity, head_count):
        self.name = name
        self.location = location
        self.total_capacity = total_capacity
        self.head_count = head_count
    
    def person_entry(self):
        self.head_count = self.head_count + 1
        
    def person_leave(self):
        self.head_count = self.head_count - 1


p1 = Pub("Dog and Hedgehog", "Dadlington", 55, 0)

print(p1.head_count)

for i in range(10):
    p1.person_entry()

print(p1.head_count)