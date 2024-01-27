import random, os
import pickle
import sys

def random_fkt():      # make sense together with test ;)
    z = os.path.basename(os.path.realpath(__file__))
    print(f"this is a random function from {z}")
    print(f"Game.py: this is the called function {sys.argv[0]}")
    print(f"Game.py: this is the first param {sys.argv[1]}")

class Board:
    def __init__(self, player, width=10, height=10):
        self.path = os.path.dirname(os.path.realpath(__file__))
        print(self.path)
        self.width = width
        self.height = height
        self.x = self.width // 2
        self.y = self.height // 2
        self.str_exit_game = "You decided to quit the game. See you next time!"
        self.d_decision = {
            "help": self.help_for_user,
            "exit": self.exit_by_user,
            "w": self.forward,
            "s": self.backward,
            "a": self.left,
            "d": self.right,
            "bag": player.get_bag_items,
            "trank": player.use_trank,
            "values": player.get_values,
            "save": self.save_game,
            "load": self.load_game,
            "position": self.get_position
        }
    
    def get_position(self):
        print(f"position in x is: {self.x}")
        print(f"position in y is: {self.y}")
                
    def save_game(self):
        self.save_state_items = [Player.name,
                                 Player.level,
                                 Player.strength,
                                 Player.max_health,
                                 Player.health,
                                 Player.max_amor,
                                 Player.amor,
                                 Player.EP,
                                 Player.EP_next_level,
                                 self.x,
                                 self.y,
                                 Player.bag
                                 ]
        with open(f"{self.path}/save.txt", "w") as file:
            for i in range(len(self.save_state_items)):
                # print(self.save_state_items[i])
                file.write(str(self.save_state_items[i]) + ", ")
        print("Game is saved.")

    def load_game(self):
        with open(f"{self.path}/save.txt", "r") as file:
            for line in file:
                first_split = line.split("{")
                loaded_safe_state_items = first_split[0].split(", ")
                # print(loaded_safe_state_items)
            Player.name          = loaded_safe_state_items[0]
            Player.level         = int(loaded_safe_state_items[1])
            Player.strength      = int(loaded_safe_state_items[2])
            Player.max_health    = int(loaded_safe_state_items[3])
            Player.health        = int(loaded_safe_state_items[4])
            Player.max_amor      = int(loaded_safe_state_items[5])
            Player.amor          = int(loaded_safe_state_items[6])
            Player.EP            = int(loaded_safe_state_items[7])
            Player.EP_next_level = int(loaded_safe_state_items[8])
            self.x               = int(loaded_safe_state_items[9])
            self.y               = int(loaded_safe_state_items[10])
            close = first_split[1].replace(" ","").replace("'","").replace("}","").split(",")
            close.pop()
            # print(close)
            for i in close:
                Player.bag[i.split(":")[0]] = int(i.split(":")[1])
        print("Game is loaded.")
                    
    def help_for_user(self):
        for key in self.d_decision:
            print(f"Input {key} to get {self.d_decision[key].__name__}.")

    def exit_by_user(self):
        print(self.str_exit_game)

    def userinput_is_correct(self, decision, who_called_me):
        if decision.lower() in self.d_decision and who_called_me == "player":
            return True
        elif (decision.lower() ==""   or 
              decision.lower() =="y"  or
              decision.lower() =="n") and who_called_me== "use_trank":
            return True
        else:
            print("I couldn't understand your input! Try again...")
            return False

    def action(self, decision):
        if decision.lower() == "save" or decision.lower() == "load":
            self.d_decision[decision]()
        else:
            self.d_decision[decision]()

    def debug(self):
        print(f"DEBUG:{self.x}, {self.y}")

    def forward(self):
        if self.y == self.height:
            print("You are at the ocean and there is no possibility to go further.")
        else:
            self.y += 1
            print("Player is moving one step forward.")
            # self.debug()

    def backward(self):
        if self.y == 0:
            print("You can see the Mountains and there is no way to cross them.")
        else:
            self.y -= 1
            print("Player is moving one step backwards.")
            # self.debug()

    def left(self):
        if self.x == 0:
            print("You are at the border of your landscape and not allowed to cross it.")
        else:
            self.x -= 1
            print("Player is moving one step left.")
            # self.debug()

    def right(self):
        if self.x == self.width:
            print("You are at the border of your landscape and not allowed to cross it.")
        else:
            self.x += 1
            print("Player is moving one step right.")
            # self.debug()
    
    def create_org(self, Level):
        if Level == 0:
            return Org("Org Level 1", 50, 50, 5, 5)
        elif Level == 1:
            return Org("Org Level 2", 100, 100, 10, 10)
        elif Level == 2:
            return Org("Org Level 3", 150, 150, 20, 15)

    def choose_org(self):
        if Player.level < 5:
            return self.create_org(random.randint(0, 1))
        else:
            return self.create_org(random.randint(0, 2))

    def list_of_orgs(self):
        if 1 == random.randint(1, 2):
            orgs_count = random.randint(1, 3)
            orgs = []
            for i in range(orgs_count):
                orgs.append(self.choose_org())
            print("It is time for a fight because You can see:")
            for i in orgs:
                print(i.name)
                # print(i)
            return orgs
        print("There is nothing to see. Only the wide area of wildness.")


class Character:
    def __init__(self, name, max_armor, max_health, strength):
        self.name = name
        self.max_amor = max_armor
        self.max_health = max_health
        self.strength = strength
    
    def fight(self, enemy):
        print(f"{self.name} attacks {enemy.name} with {self.strength}strength")
        enemy.health -= self.strength
        if enemy.health <= 0:
            # print("Org" in enemy.name)
            if "Org" in enemy.name:
                # died_org = l_orgs.pop(0)
                print(f"{enemy.name} died.")
                enemy.dropped_items(enemy, Player)
                self.ep_increase(enemy)
            else:
                print("Game Over")
                exit()
        else:
            print(f"{enemy.name} has {enemy.health}/{enemy.max_health} left.")



class ClassPlayer(Character):
    def __init__(self, name, max_armor, max_health, strength, amor, health):
        self.amor = amor
        self.health = health
        self.level = 1
        self.EP = 0
        self.bag = {"Trank": 0,
                    "other": 0}
        self.EP_next_level = 20
        super(ClassPlayer, self).__init__(name, max_armor, max_health, strength)

    def increase_values(self):
        self.level += 1
        self.strength += 2 * self.level
        self.EP_next_level *= 2
        self.max_health = int(self.max_health * 1.2)
        self.max_amor = int(self.max_amor * 1.2)

    def get_values(self):
        print(f"Level:    {self.level}")
        print(f"Strength: {self.strength}")
        print(f"Health:   {self.health}/{self.max_health}")
        print(f"Amor:     {self.amor}/{self.max_amor}")
        print(f"EP:       {self.EP}/{self.EP_next_level}")

    def level_up(self):
        while self.EP >= self.EP_next_level:
            self.increase_values()
            print(f"Be Happy! Your level increased by 1. Your current level is: {self.level}.")

    def insert_stuff_in_bag(self, items):
        # print(items[0])
        for key in items:
            if key not in self.bag:
                self.bag[key] = items[key]
            else:
                self.bag[key] += items[key]
            print(f"You got {items[key]} time(s) {key}")

    def get_bag_items(self):
        if not self.bag == {}:
            print(f"Your bag includes following items:")
            for key in self.bag:
                print(f"{key} {self.bag[key]}")
        else:
            print("Your bag is empty")

    def ep_increase(self, died_org):
        self.EP += died_org.ep_gain
        print(f"You gained {died_org.ep_gain}EP!")
        self.level_up()
        
    def auto_trank(self):
        if self.health < self.max_health and self.bag["Trank"] > 0:
            self.health += 20
            if self.health > self.max_health:
                self.health = self.max_health
            print(f"{self.health}/{self.max_health}")
            self.bag["Trank"] -= 1
            return True
        else:
            print(f"You run out of Tranks!")
            return False
                
    def use_trank(self):
        switch = True
        while switch:
            if self.bag["Trank"] == 0:
                print(f"Your bag is not filled with any Trank! It seams you are fucked up!")
                switch = False
                continue
            elif self.health == self.max_health:
                print(f"It is not needed to use Trank. You have {self.health}/{self.max_health}.")
                switch = False
                continue
            is_auto_refill = input(f"Do you want to refill to 100%? Situation: {self.health}/{self.max_health}[Y/n]: ")
            user_decision_is_true = Board.userinput_is_correct(game, is_auto_refill, "use_trank")
            if  user_decision_is_true and is_auto_refill.lower() == "n":
                self.auto_trank()
                switch = False
            elif user_decision_is_true:
                while switch and self.health < self.max_health:
                    switch = self.auto_trank()                    
                switch = False
                

class Org(Character):
    def __init__(self, name, max_health, health, strength, ep_gain):
        self.health = health
        self.ep_gain = ep_gain
        self.items = {"Org Level 1": {"Trank": 1},
                      "Org Level 2": {"Trank": 2},
                      "Org Level 3": {"Trank": 3, "Amor": 1}}
        super(Org, self).__init__(name, max_health, health, strength)
        
#TODO droped items quality and quantaty level dependency
 
    def dropped_items(self, died_org, player):
        if 1 == random.randint(1, 2):
            player.insert_stuff_in_bag(self.items[died_org.name])
        else:
            print(f"{player.name} got nothing from {died_org.name}")

if __name__=="__main__":
    Player = ClassPlayer("Paul", 100, 100, 50, 100, 100)
    game = Board(Player)
    
    print("If you would like to have more information input 'help'.")
    while True:
        t = input("Next movement?: ").lower()
        if game.userinput_is_correct(t, "player"):
            if t.lower() == "exit":
                break
            game.action(t)
            if t.lower() == "a" or \
            t.lower() == "w" or \
            t.lower() == "s" or \
            t.lower() == "d":
                l_orgs = game.list_of_orgs()
                while l_orgs:
                    Player.fight(l_orgs[0])
                    if l_orgs[0].health <= 0:
                        l_orgs.pop(0)
                    for org in l_orgs:
                        org.fight(Player)
        