class Room:
    def __init__(self, name, description, list_of_entities = None):
        self.name = name
        self.description = description
        self.list_of_entities = list_of_entities
        if list_of_entities is not None:
            for i in self.list_of_entities:
                i.set_Room(self)
    
    def delete_entity(self, entity):
        self.list_of_entities.remove(entity)
    
    def set_ways_to(self, ways):
        self.ways = ways
        
    def show_avaliable_rooms(self):
        k=1
        for i in self.ways:
            print(f'{k}: {i.name} | {i.description}')
            k+=1
        print(f'{k}: Залишитися')
    
class Item:
    def __init__(self, name, description, durability):
        self.name = name
        self.description = description
        self.durability = durability
    def __str__(self):
        return f'{self.name} | {self.description}. Durability: {self.durability}'

class Food(Item):
    def __init__(self, name, description, durability, health):
        super().__init__(name, description, durability)
        self.health = health

    def use_food(self, hero):
        hero.health = min(hero.health + self.health, Hero.max_health)
        self.durability -=1
        if self.durability<1:
            hero.inventory.remove(self)
    def __str__(self):
        return f'{self.name} | {self.description}. Durability: {self.durability}. Healing: {self.health}'

class Weapon(Item):
    def __init__(self, name, description, durability, damage):
        super().__init__(name, description, durability)
        self.damage = damage
    def use_weapon(self, hero, enemy):
        self.durability-=1
        enemy.health-=self.damage
        if self.durability<1:
            hero.inventory.remove(self)
            hero.current_weapon = Weapon("Кулаки", "На жаль, ти небагато займався споротм...", 100000000, 10)
    def __str__(self):
        return f'{self.name} | {self.description}. Durability: {self.durability}. Damage: {self.damage}'

class Entity:
    def __init__(self, name, health, replicas = None, greetings = None):
        self.name = name
        self.health = health
        self.replicas = replicas
        self.greetings = greetings
    def set_Room(self, room):
        self.location = room
    def answer_to_hero(self, text):
        if self.replicas is not None:
            print(self.replicas[text])
            return self.replicas[text]
    def start_talk(self):
        print(self.greetings)

class Hero(Entity):
    max_health = 100
    def take_action(self):
        print("---------------------------------")
        print(f'Поточне місцезнаходження: {self.current_room.name}')
        print(f'talk | move | fight | inventory')
        print("---------------------------------")
        action = input(">>> ")
        if action == "talk":
            entity = None
            if self.current_room == None:
                return None
            for i in self.current_room.list_of_entities: 
                if i.replicas is not None:
                    entity = i
            if entity is None:
                return None
            print("1:", entity.name)
            print("2: Піти")
            action = int(input(">>> "))
            if action == 2:
                return None
            if action == 1:
                entity.start_talk()
            self.talking(entity)
        elif action == "move":
            self.current_room.show_avaliable_rooms()
            action = int(input(">>> "))
            if action == len(self.current_room.ways)+1:
                return None
            else:
                self.current_room = self.current_room.ways[action-1]
        elif action == "fight":
            enemies = []
            k = 1
            for i in self.current_room.list_of_entities:
                if isinstance(i, Enemy):
                    enemies.append(i)
                    print(f'{k}: {i.name}')
                    k+=1
            print(f'{k}: Піти')
            if len(enemies) == 0:
                return None
            action = int(input(">>> "))
            if action == len(enemies)+1:
                return None
            else:
                self.fight(enemies[action-1])
        elif action == "inventory":
            hero.show_inventory()
                
                
            
    def __init__(self, name, health, inventory, current_room):
        super().__init__(name, health)
        self.inventory = inventory
        self.current_room = current_room
        self.alive = True
        self.current_weapon = Weapon("Кулаки", "На жаль, ти небагато займався споротм...", 100000000, 10)
        self.got_revolverr=False
        self.got_shotgun=False
        self.replicas = {"Майор": ["Навіщо ви мене викликали?", "Як дібратися до міста?", "Бувай."], 
                         "Зброєносець Свтослав":["Де знайти Гетьмана? У мене для нього секретні відомості.", "Бувай."],
                         }
    
    def talking (self, entity):
        text = ""
        while text!="Бувай.":
            if not "Проблем з бунтівниками не буде." in self.replicas["Зброєносець Свтослав"] and len(factory.list_of_entities)==0:
                self.replicas["Зброєносець Свтослав"].append("Проблем з бунтівниками не буде.")
                city.set_ways_to([barracks, factory, wild_field, hetman_palace])
            if not self.got_shotgun and not "Де знайти Гетьмана? У мене для нього секретні відомості." in self.replicas["Зброєносець Свтослав"]:
                self.replicas["Зброєносець Свтослав"].append("Є щось, щоб упевнило ворогів в моїй правоті?")
            k=1
            for i in self.replicas[entity.name]:
                print(f'{k}: {i}')
                k+=1
            action = int(input())
            text = self.replicas[entity.name][action-1]
            answer = entity.answer_to_hero(text)
            if answer == "Треба Гетьман? Є робота. Розберись з бунтівниками, тоді пропущу.":
                self.replicas["Зброєносець Свтослав"].remove("Де знайти Гетьмана? У мене для нього секретні відомості.")
            elif answer == "Чудово. Ти, можливо, врятував сотні, якщо не тисячі життів. Тепер йди до Гетьмана.":
                self.replicas["Зброєносець Свтослав"].remove("Чудово. Ти, можливо, врятував сотні, якщо не тисячі життів. Тепер йди до Гетьмана.")
            elif answer == "Тримай рушницю. З набоями біда, тому даю тільки два." and self.got_shotgun==False:
                self.got_shotgun = True
                self.inventory.append(Weapon("Двохстволка", "Надзвичайно велика порція свинцю", 2, 200))
                self.replicas["Зброєносець Свтослав"].remove("Є щось, щоб упевнило ворогів в моїй правоті?")
            elif answer == "Якщо коротко, то тобі необхідно доставити відомісті розвідки з лінії розмежування Гетьману. Він знаходиться в місті. Тримай револьвер, щоб не вмер по дорозі.":
                self.got_revolver = True
                self.inventory.append(Weapon("Револьвер", "Однієї кулі достатньо, щоб перервати підневільний подвиг існування", 8, 75))
                self.replicas["Майор"].remove("Навіщо ви мене викликали?")
    
            
        
    
    def set_current_weapon(self, weapon):
        self.current_weapon = weapon

    def show_inventory(self):
        if len(self.inventory)==0:
            print("Упс. Нічого нема")
        k=1
        for i in self.inventory:
            print(f'{k}: {i}')
            k+=1 
    def dead(self, enemy):
        print(f'{self.name} мертвий')
        self.alive=False
        # 
    def fight(self, enemy):
        fight_round = 1
        while (self.health>0 and enemy.health>0):
            print("---------------------------------")
            print(f'Хід: {fight_round}')
            print("shoot | eat | change | inventory")
            print("---------------------------------")
            print(f'Твоє здоров\'я: {self.health}')
            print(f'Твоя зброя: {self.current_weapon}')
            print("---------------------------------")
            print(enemy)
            print("---------------------------------")
            flag = False
            action = input(">>> ")
            if action == "shoot":
                hero.current_weapon.use_weapon(hero, enemy)
            elif action == "inventory":
                hero.show_inventory()
                flag=True
                fight_round-=1
            elif action == "eat":
                foods = []
                k=1
                for i in self.inventory:
                    if isinstance(i, Food):
                        foods.append(i)
                        print(f'{k}: {i}')
                        k+=1 
                print(f'{k}: Я передумав')
                if len(foods)==0:
                    flag=True
                    fight_round-=1
                    break
                action = int(input(">>> "))
                if action == len(foods)+1:
                    flag=True
                    fight_round-=1
                else:
                    foods[action-1].use_food(self)
            elif action == "change":
                weapons=[]
                k=1
                for i in self.inventory:
                    if isinstance(i, Weapon):
                        weapons.append(i)
                        print(f'{k}: {i}')
                        k+=1 
                print(f'{k}: Я передумав')     
                action = int(input(">>> "))
                if action != len(weapons)+1:
                    self.set_current_weapon(weapons[action-1])
                flag=True
                fight_round-=1
            if enemy.health>0 and not flag and not fight_round%enemy.rounds_for_move:
                enemy.fight_move(self)
            fight_round+=1
        if enemy.health<=0:
            enemy.dead()
            enemy.append_loot(hero)
    def change_room(self, new_room):
        self.current_room = new_room
        

class Enemy(Entity):
    def __init__(self, name, health, damage, rounds_for_move, replicas = None, greetings = None, loot = None):
        super().__init__(name, health, replicas, greetings)
        self.damage = damage
        self.rounds_for_move = rounds_for_move
        self.location = None
        self.loot = loot

    def dead(self):
        print(f'{self.name} мертвий')
        self.location.delete_entity(self)        

    def append_loot(self, enemy):
        if self.loot is not None:
            print(f'О, випало: {self.loot.name}')
            enemy.inventory.append(self.loot)

    def fight_move(self, enemy):
        enemy.health-=self.damage
        if enemy.health<=0:
            enemy.dead(self)

    def __str__(self):
        return f'{self.name} | {self.health} | {self.damage} | {self.rounds_for_move}'

major_talks = {"Навіщо ви мене викликали?":"Якщо коротко, то тобі необхідно доставити відомісті розвідки з лінії розмежування Гетьману. Він знаходиться в місті. Тримай револьвер, щоб не вмер по дорозі.",
               "Як дібратися до міста?": "Через дике поле!",
               "Бувай.": "Бувай."}
major = Entity("Майор", 100, major_talks, "Чувай")
pub_room = Room("Корчма", "Тут можна випити", [major])
hero = Hero("Безіменний солдат", 100, [], pub_room)


caban1 = Enemy("Кабан", 100, 25, 2, loot = Food("М\'ясо кабанчика", "Смакота!", 1, 100))
caban2 = Enemy("Кабан", 100, 25, 2, loot = Food("М\'ясо кабанчика", "Смакота!", 1, 100))
wild_field = Room("Дике поле", "Будь обережним", [caban1, caban2])

city = Room("Місто", "Київ такий красивий...", [])

master_talks = {"Де знайти Гетьмана? У мене для нього секретні відомості." : "Треба Гетьман? Є робота. Розберись з бунтівниками, тоді пропущу.",
"Є щось, щоб упевнило ворогів в моїй правоті?" :"Тримай рушницю. З набоями біда, тому даю тільки два.",
"Проблем з бунтівниками не буде." :
"Чудово. Ти, можливо, врятував сотні, якщо не тисячі життів. Тепер йди до Гетьмана.",
"Бувай.": "Нехай щастить."}
master_in_arms = Entity("Зброєносець Свтослав", 100, master_talks, "Слухаю")
barracks = Room("Каземати", "Багато військових", [master_in_arms])

glovar = Enemy("Ленін з револьвером", 500, 75, 4)
podsos1 = Enemy("Червоноармієць з гвинтівкою", 150, 50, 1, loot = Weapon("Гвинтівка", "Mauser98k", 5, 50))
podsos2 = Enemy("Косоокий кулеметник", 200, 60, 3, loot = Food("Сирна косичка", "Улюблена страва у потягах", 2, 20))
podsos3 = Enemy("Комуністичний щур", 50, 20, 1)
factory = Room("Завод", "Тут розпочалося повстання", [glovar, podsos1, podsos2, podsos3])

hetman_palace = Room("Палац Гетьмана", "Кошерно", )

pub_room.set_ways_to([wild_field])
wild_field.set_ways_to([pub_room, city])
city.set_ways_to([barracks, factory, wild_field])
barracks.set_ways_to([city])
factory.set_ways_to([city])

if __name__ == "__main__":    
    while hero.alive:
        if hero.current_room == hetman_palace:
            hero.alive = False
            print("Вітаю. Ти доставив дані Гетьману. Тепер є вдосталь часу, щоб визначитися зі стратегією")
        else:
            hero.take_action()
