from virus import Virus
from logger import Logger
from person import Person
import random
import sys


class Simulation(object):
    ''' Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments when file is run.
    Simulates the spread of a virus through a given population.  The percentage of the
    population that are vaccinated, the size of the population, and the amount of initially
    infected people in a population are all variables that can be set when the program is run.
    '''
    # TODO: This might break the logger. Keep an eye out because the args changed.

    def __init__(self, population_size, vacc_percentage,  virus, initial_infected=1):
        ''' Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and should have a unique _id value.
        The vaccination percentage represents the total percentage of population
        vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected with the disease.
        The total infected people is the running total that have been infected since the
        simulation began, including the currently infected people who died.
        You will also need to keep track of the number of people that have died as a result
        of the infection.
        All arguments will be passed as command-line arguments when the file is run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        '''
        self.population = []  # List of Person objects
        self.population_size = population_size  # Int
        self.virus = virus  # Virus object
        self.initial_infected = initial_infected  # Int
        self.total_infected = self.initial_infected  # Int
        self.current_infected = self.initial_infected  # Int
        self.vacc_percentage = vacc_percentage  # float between 0 and 1
        self.total_dead = 0  # Int
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            self.virus.name, population_size, vacc_percentage, initial_infected)
        self.logger = Logger(self.file_name)
        self.newly_infected = []
        self._create_population = self._create_population()

    def _create_population(self):
        '''This method will create the initial population.
            Returns:
                list: A list of Person objects.
        '''
        # Should return a 0.xx value - Vacc percentage
        vacc_percentage = self.vacc_percentage

        # The number of people to vaccinate
        num_to_vac = int(self.population_size * vacc_percentage)

        # Number of infected people
        num_to_infect = self.initial_infected

        # healthy percentage
        num_to_create_norm = self.population_size - \
            (num_to_infect + num_to_vac)

        counter = 1
        for i in range(0, num_to_vac):
            counter += 1
            self.population.append(Person(i, True, None))

        for i in range(counter, num_to_infect + counter):
            counter += 1
            self.population.append(Person(i, False, self.virus))

        for i in range(counter, num_to_create_norm + counter):
            self.population.append(Person(i, False, None))

    def _simulation_should_continue(self):
        ''' The simulation should only end if the entire population is dead
        or everyone is vaccinated.
            Returns:
                bool: True for simulation should continue, False if it should end.
        '''
        # Reset values to avoid early term
        self.total_dead = 0
        self.current_infected = 0

        # Get a list of people who are alive
        # TODO: Could break logic, may need to rewrite again
        for person in self.population:
            # get a count of all the dead peopl
            if person.is_alive == False:
                self.total_dead += 1

            # self.current_infected will be 0 if everyone is vaccinated and alive - will ignore dead people
            if person.infection and person.is_alive:
                self.current_infected += 1

        # First check if total dead is same length of population, meaning everyone is dead
        if self.total_dead == len(self.population):
            return False
        # If none are infected then either all dead or vaccinated
        elif self.current_infected == 0:
            return False
        else:
            # In other cases return True
            return True

    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        time_step_counter = 0
        should_continue = self._simulation_should_continue()
        self.logger.write_metadata(self.population_size, self.vacc_percentage,
                                   self.virus.name, self.virus.mortality_rate, self.virus.repro_rate)

        while should_continue:
            self.time_step()

            for person in self.population:
                self.logger.log_infection_survival(
                    person, person.did_survive_infection(self.virus))

            self._infect_newly_infected()

            time_step_counter += 1
            self.logger.log_time_step(time_step_counter)
            should_continue = self._simulation_should_continue()

        print(f'The simulation has ended after {time_step_counter} turns.')
        # Return for tests
        return f'The simulation has ended after {time_step_counter} turns.'

    def time_step(self):
        ''' This method should contain all the logic for computing one time step
        in the simulation.
        This includes:
            1. 100 total interactions with a randon person for each infected person
                in the population
            2. If the person is dead, grab another random person from the population.
                Since we don't interact with dead people, this does not count as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
            '''
        # Get a list of alive people
        living_people = [x for x in self.population if x.is_alive]

        for person in living_people:
            interaction = 0
            if person.infection:
                while interaction <= 100:
                    rand_person = random.choice(living_people)
                    self.interaction(person, rand_person)
                    interaction += 1

    def interaction(self, person, random_person):
        '''This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.
        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        '''
        # Assert statements are included to make sure that only living people are passed in as params
        assert person.is_alive == True
        assert random_person.is_alive == True

        # Check to see if the person is infected
        if random_person.is_vaccinated:
            # Logs that the user is vaccinated
            self.logger.log_interaction(
                person, random_person, False, True, False)

        elif random_person.infection is not None:
            # Logs that the random_user did not get infected because they already are.
            self.logger.log_interaction(
                person, random_person, True, False, False)

        elif random_person.infection is None and random_person.is_vaccinated == False and random_person._id is not person._id:
            # Generate random value to be used to compare against repro rate
            rand_val = random.random()
            if rand_val < self.virus.repro_rate:
                # Random person got infected by the virus
                self.newly_infected.append(random_person._id)
                # Log that the user got infected
                self.logger.log_interaction(
                    person, random_person, False, False, True)
                # For testing purposes
            else:
                # Got lucky and resisted the virus
                self.logger.log_interaction(
                    person, random_person, False, False, False)
            return rand_val

    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''

        for user_id in self.newly_infected:
            for person in self.population:
                if person._id == user_id:
                    person.infection = self.virus
        self.newly_infected = []


if __name__ == "__main__":
    # p3 simulation.py Ebola 0.25 0.70 100 0.90 10
    params = sys.argv[1:]
    print(params)
    virus_name = str(params[0])
    repro_num = float(params[1])
    mortality_rate = float(params[2])

    population_size = int(params[3])
    vacc_percentage = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(virus_name, repro_num, mortality_rate)
    sim = Simulation(population_size, vacc_percentage, virus, initial_infected)

    sim.run()
