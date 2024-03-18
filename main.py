class Player:
    def __init__(self, name, cash, level):
        self.name = name
        self.cash = cash
        self.level = level
        self.xp = 0
        self.required_xp_to_level_up = 100
        self.level_checker()

    def add_cash(self, cash_to_add):
        self.cash += cash_to_add

    def set_cash(self, cash_to_set):
        self.cash += cash_to_set

    def set_xp(self, xp_to_set):
        self.xp = xp_to_set
        self.level_up()

    def add_xp(self, xp_to_add):
        self.xp += xp_to_add
        self.level_up()

    def level_checker(self):
        self.required_xp_to_level_up = (self.level ** 5)
        self.level_up()

    def increment_level(self):
        self.level += 1

    def level_up(self):
        if self.xp >= self.required_xp_to_level_up:
            self.increment_level()
            self.level_checker()

    def print_info(self):
        print(f"Cash: {self.cash}\nLevel: {self.level}\nXP: {self.xp}\nRequired XP for LEVEL UP: {self.required_xp_to_level_up}")


player = Player("Default", 1000, 1)
player.set_xp(123)
player.print_info()