import beverages
import random

class CoffeeMachine:
    def __init__(self):
        self.obsolescence = 0

    class EmptyCup(beverages.HotBeverage):
        def __init__(self):
            self.name = "empty cup"
            self.price = 0.90

        def description(self):
            return ("An empty cup ?! Gimme my money back!")

    class BrokenMachineException(Exception):
        def __init__(self):
            super().__init__("This coffee machine has to be repaired.")

    def repair(self):
        self.obsolescence = 0

    def serve(self, beverage):
        if self.obsolescence >= 10: 
            raise self.BrokenMachineException()
        self.obsolescence += 1
        if random.randint(0, 1) == 1: 
            return (beverage())
        else:
            return (self.EmptyCup())

if __name__ == "__main__":
    coffeeMachine = CoffeeMachine()
    hotBeverages =  [beverages.HotBeverage, beverages.Coffee, beverages.Tea, beverages.Chocolate, beverages.Cappuccino]
    try:
        for i in range(0, 15):
            print(coffeeMachine.serve(random.choice(hotBeverages)))
    except Exception as e:
        print (e)
    coffeeMachine.repair()
    try:
        print(coffeeMachine.serve(beverages.Coffee))
        print(coffeeMachine.serve(beverages.Chocolate))
        print(coffeeMachine.serve(beverages.Tea))
        print(coffeeMachine.serve(beverages.Coffee))
        print(coffeeMachine.serve(beverages.Cappuccino))
        print(coffeeMachine.serve(beverages.Coffee))
        print(coffeeMachine.serve(beverages.Tea))
        print(coffeeMachine.serve(beverages.Coffee))
        print(coffeeMachine.serve(beverages.Chocolate))
        print(coffeeMachine.serve(beverages.Cappuccino))
        print(coffeeMachine.serve(beverages.Coffee))
    except Exception as e: 
        print (e)