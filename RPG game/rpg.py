def log_action(func):
    def wrapper(self, *args, **kwargs):
        print(self.name, "→", func.__name__)
        return func(self, *args, **kwargs)
    return wrapper


class Character:
    count = 0

    def __init__(self, name, hp=100, level=1):
        self.name = name
        self.hp = hp
        self.level = level
        Character.count += 1

    def __str__(self):
        return f"{self.name} (Lv {self.level}, HP {self.hp})"

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    @property
    def is_alive(self):
        return self.hp > 0

    def attack(self, target):
        target.take_damage(5)

    @classmethod
    def from_string(cls, text):
        name, hp = text.split(";")
        return cls(name, hp=int(hp))

    @staticmethod
    def is_valid_name(name):
        return 2 <= len(name) <= 20

    def __eq__(self, other):
        return self.name == other.name and self.level == other.level


class Warrior(Character):
    def __init__(self, name, hp=100, level=1, strength=10):
        super().__init__(name, hp, level)
        self.strength = strength

    @log_action
    def attack(self, target):
        target.take_damage(self.strength)


class Mage(Character):
    def __init__(self, name, hp=100, level=1, mana=50):
        super().__init__(name, hp, level)
        self.mana = mana

    @log_action
    def attack(self, target):
        if self.mana >= 10:
            self.mana -= 10
            target.take_damage(20)
        else:
            super().attack(target)

    def __str__(self):
        return super().__str__() + f" MP {self.mana}"


class HealerMixin:
    @log_action
    def heal(self, target, amount):
        target.hp += amount


class Priest(HealerMixin, Mage):
    pass


class Inventory:
    def __init__(self):
        self.items = []

    def add(self, **item):
        self.items.append(item)

    def find(self, **filters):
        return [
            item for item in self.items
            if all(item.get(key) == value for key, value in filters.items())
        ]

    def __len__(self):
        return len(self.items)


def battle(a, b):
    while a.is_alive and b.is_alive:
        a.attack(b)
        if b.is_alive:
            b.attack(a)
        print(a)
        print(b)
        print("-" * 30)
    if a.is_alive:
        return a
    return b


if __name__ == "__main__":
    tariel = Warrior("Tariel", hp=120, strength=15)
    nestan = Mage("Nestan", hp=80, mana=50)
    tariel.attack(nestan)
    print(nestan)
    print(nestan.is_alive)
    print(Character.count)

    p = Priest("Nestan", hp=60)
    w = Warrior.from_string("Tariel;120")
    p.heal(w, 30)
    print(w)
    print(type(w).__name__)
    print(Character.is_valid_name("T"))
    print(Character("A") == Character("A"))
    print(Priest.__mro__)

    inv = Inventory()
    inv.add(name="sword", kind="weapon", power=10)
    inv.add(name="potion", kind="heal", power=30)
    print(len(inv))
    print(inv.find(kind="weapon"))
    print(inv.find(kind="heal", power=30))

    winner = battle(Warrior("Tariel", hp=120), Mage("Nestan", hp=80))
    print(f"gamarjvebuli: {winner.name}")