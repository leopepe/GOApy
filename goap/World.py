class World:

    def __init__(self, facts: list):
        self.facts = facts

    def add_fact(self, fact: str):
        self.facts.append(fact)

    def remove_fact(self, fact: str):
        self.facts.remove(fact)

    def clear_facts(self):
        self.facts.clear()

    def get_facts(self):
        return self.facts

