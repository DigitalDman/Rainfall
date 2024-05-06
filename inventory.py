import pygame
#Some code derived from: https://youtu.be/1q_0l71Ln7I#

# Information about each type (icon, value, stack size, etc.).
class ItemType:
    def __init__(self, name, icon, stack_size=1) -> None:
        self.name = name
        self.icon_name = icon
        self.icon = pygame.image.load(icon)
        self.value = 0
        self.weight = 0
        # Determines how much of one item can be held in a single slot.
        self.stack_size = stack_size

# Can hold a quantity of an item.
class ItemSlot:
    def __init__(self) -> None:
        self.type = None
        self.amount = 0

# Has a certain number of slots for items.
class Inventory:
    # Creates new inventory
    def __init__(self, capacity) -> None:
        self.capacity = capacity
        self.taken_slots = 0
        self.slots = []
        for _ in range (self.capacity):
            self.slots.append(ItemSlot())
        self.listener = None

    # Lets a listener know the inventory changed. Useful for our UI.
    def notify (self):
        pass

    # Attempts to add a certain amount of an item to the inventory. Returns any excess items it couldn't add.
    def add(self, item_type, amount=1):
        # First sweep for any open stacks
        if item_type.stack_size > 1:
            for slot in self.slots:
                if slot.type == item_type:
                    add_amo = amount
                    if add_amo > item_type.stack_size - slot.amount:
                        add_amo = item_type.stack_size - slot.amount
                    slot.amount += add_amo
                    amount -= add_amo
                    if amount <= 0:
                        self.notify()
                        return 0
        # Next, place the item in the next slot
        for slot in self.slots:
            if slot.type == None:
                slot.type = item_type
                if item_type.stack_size < amount:
                    slot.amount = item_type.stack_size
                    self.notify()
                    return self.add(item_type, amount - item_type.stack_size)
                else:
                    slot.amount = amount
                    self.notify()
                    return 0

        return amount

    # Attempts to remove a certain amount of an item to the inventory. Returns what it wasn't able to remove.
    def remove (self, item_type, amount = 1):
        found = 0
        for slot in self.slots:
            if slot.type == item_type:
                if slot.amount < amount:
                    found += slot.amount
                    slot.amount = 0
                    slot.type = None
                    self.notify()
                    continue
                elif slot.amount == amount:
                    found += amount
                    slot.amount = 0
                    slot.type = None
                    self.notify()
                    return found
                else:
                    found += amount
                    slot.amount -= amount
                    self.notify()
                    return found
        return found
    
    # Returns whether a certain amount of an item is present in the inventory.
    def has (self, item_type, amount = 1):
        found = 0
        for slot in self.slots:
            if slot.type == item_type:
                found += slot.amount
                if found >= amount:
                    return True
        return False
    
    def amount_item(self, item_type):
        found = 0
        for slot in self.slots:
            if slot.type == item_type:
                return slot.amount

    # Returns the first slot number of where an item is.
    def get_index(self, item_type):
        for index, slot in enumerate(self.slots):
            if slot.type == item_type:
                return index
        return -1
    
    def __str__(self):
        s = ""
        for i in self.slots:
            if i.type is not None:
                s += str(i.type.name) + ": " + str(i.amount) + "\t"
            else:
                s += "Empty slot\t"
        return s

    def get_free_slots(self):
        return self.capacity - self.taken_slots
    
    def is_full(self):
        return self.taken_slots == self.capacity
    
    def get_weight(self):
        weight = 0
        for i in self.slots:
            weight += i.weight * i.amount
        return weight
    
    def get_value(self):
        value = 0
        for i in self.slots:
            value += i.value * i.amount
        return value

# An item that can be picked up.
# class DroppedItem(Trigger):
    pass