from random import uniform, random
from virus import Virus


class Person(object):
    ''' Person objects will populate the simulation. '''

    def __init__(self, _id, is_vaccinated, infection=None):
        ''' 
        If person is chosen to be infected when the population is created, the simulation
        should instantiate a Virus object and set it as the value
        self.infection. Otherwise, self.infection should be set to None.
        '''
        self._id = int(_id)  # int
        self.is_alive = True  # boolean
        self.is_vaccinated = bool(is_vaccinated)  # boolean
        self.infection = infection

    def did_survive_infection(self, virus):
        ''' Generate a random number and compare to virus's mortality_rate.
        If random number is smaller, person dies from the disease.
        If Person survives, they become vaccinated and they have no infection.
        Return a boolean value indicating whether they survived the infection.
        '''
        if self.infection:
            god = random()
            if god < self.infection.mortality_rate:
                self.is_alive = False
            else:
                self.is_vaccinated = True
                self.infection = None

        return self.is_alive


def test_vacc_person_instantiation():
    person = Person(1, True)
    assert person._id == 1
    assert person.is_alive is True
    assert person.is_vaccinated is True
    assert person.infection is None


def test_not_vacc_person_instantiation():
    gary = Person(2, False)
    assert gary._id == 2
    assert gary.is_alive is False


def test_sick_person_instantiation():
    virus = Virus("Dysentery", 0.7, 0.2)
    person = Person(3, False, virus)

    assert person._id == 3
    assert person.is_vaccinated is False
    assert person.infection == virus


def test_did_survive_infection():
    virus = Virus("HIV", 0.8, 0.2)
    person = Person(4, False, virus)

    # Resolve whether the Person survives the infection or not
    survived = person.did_survive_infection(virus)
    if survived:
        assert person.is_alive is True
        assert person.is_vaccinated is True
        assert person.infection is None

    else:
        assert person.is_alive is False
        assert person.is_vaccinated is False
        assert person.infection is False
        assert person.infection == virus


if __name__ == "__main__":
    test_vacc_person_instantiation()
    test_not_vacc_person_instantiation()
    test_sick_person_instantiation()
