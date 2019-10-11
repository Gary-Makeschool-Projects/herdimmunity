from virus import Virus
from person import Person
from simulation import Simulation
import random
random.seed(42)


def test_create_simulation():
    virus = Virus("HIV", 0.60, 0.30)
    assert virus.name == "HIV"
    assert virus.repro_rate == 0.60
    assert virus.mortality_rate == 0.30

    simulation = Simulation(500, 0.70, virus, 2)

    assert simulation.population_size == 500
    assert simulation.virus.name == "HIV"
    assert simulation.initial_infected == 2
    assert simulation.vacc_percentage == 0.70
    assert simulation.file_name == 'HIV_simulation_pop_500_vp_0.7_infected_2.txt'


def test_create_population():
    virus = Virus("HIV", 0.60, 0.30)
    assert virus.name == "HIV"
    assert virus.repro_rate == 0.60
    assert virus.mortality_rate == 0.30

    simulation = Simulation(500, 0.70, virus, 2)
    assert simulation.population_size == 500
    assert simulation.virus.name == "HIV"
    assert simulation.initial_infected == 2
    assert simulation.vacc_percentage == 0.70

    normal_count = 0
    vacc_count = 0
    infec_count = 0
    for person in simulation.population:
        if person.is_vaccinated:
            vacc_count += 1
        elif person.infection:
            infec_count += 1

    assert normal_count == 0 and vacc_count == 350 and infec_count == 2


def test_simulation_should_continue_true():
    virus = Virus("HIV", 0.60, 0.30)
    simulation = Simulation(500, 0.70, virus, 2)
    assert simulation._simulation_should_continue() is True


def test_simulation_should_continue_false():
    virus = Virus("HIV", 0.60, 0.30)
    simulation = Simulation(500, 0.70, virus, 2)

    for person in simulation.population:
        person.is_alive = False

    assert simulation._simulation_should_continue() is False


def test_simulation_should_continue_vaccinated():
    virus = Virus("HIV", 0.60, 0.30)
    simulation = Simulation(500, 0.70, virus, 2)

    assert simulation._simulation_should_continue() is True


def test_interaction():
    virus = Virus("HIV", 0.60, 0.30)
    simulation = Simulation(500, 0.70, virus, 2)

    person1 = Person(1, False, virus)
    person2 = Person(2, False, None)

    random = simulation.interaction(person1, person2)

    if random < virus.repro_rate:
        assert simulation.newly_infected[0] == 2
    else:
        assert len(simulation.newly_infected) == 0


def test_run_func():
    virus = Virus("HIV", 0.60, 0.30)
    simulation = Simulation(500, 0.70, virus, 2)
    random.seed(42)
    answer = simulation.run()
    assert answer == 'The simulation has ended after 4 turns.'
