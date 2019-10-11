import os
from person import Person
from virus import Virus


class Logger(object):
    ''' Utility class responsible for logging all interactions during the simulation. '''
    # TODO: Write a test suite for this class to make sure each method is working
    # as expected.

    # PROTIP: Write your tests before you solve each function, that way you can
    # test them one by one as you write your class.

    def __init__(self, file_name):
        self.file_name = file_name

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       repro_rate):
        '''
        The simulation class should use this method immediately to log the specific
        parameters of the simulation as the first line of the file.
        '''
        with open(self.file_name, 'w') as f:
            msg = f'Population Size: {pop_size}    Vaccination Percentage: {vacc_percentage}    Virus: {virus_name}    Mortality Rate: {mortality_rate}    Basic Reproduction Number: {repro_rate}\n'
            f.write(msg)

    def log_interaction(self, person, random_person, random_person_sick=None,
                        random_person_vacc=None, did_infect=None):
        '''
        The Simulation object should use this method to log every interaction 
        a sick person has during each time step.
        '''
        with open(self.file_name, 'a') as f:
            if did_infect and not random_person_vacc and not random_person_sick:
                msg = f"{person._id} infects {random_person._id}.\n"
                f.write(msg)
            elif not did_infect:
                if random_person_vacc:
                    msg = f"{person._id} didn't infect {random_person._id} because they are already vaccinated.\n"
                    f.write(msg)
                elif random_person_sick:
                    msg = f"{person._id} didn't infect {random_person._id} because they are already sick.\n"
                    f.write(msg)
                else:
                    msg = f"{person._id} didn't infect {random_person._id} because they resisted the virus.\n"
                    f.write(msg)

    def log_infection_survival(self, person, did_survive_infection):
        ''' The Simulation object uses this method to log the results of every
        call of a Person object's .did_survive_infection() method.
        The format of the log should be:
            "{person.ID} died from infection\n" or "{person.ID} survived infection.\n"
        '''
        with open(self.file_name, 'a') as f:
            if did_survive_infection:
                msg = f"{person._id} survived infection.\n"
                f.write(msg)
            elif not did_survive_infection:
                msg = f"{person._id} died from infection.\n"
                f.write(msg)

    def log_time_step(self, time_step_number):
        ''' STRETCH CHALLENGE DETAILS:
        If you choose to extend this method, the format of the summary statistics logged
        are up to you.
        At minimum, it should contain:
            The number of people that were infected during this specific time step.
            The number of people that died on this specific time step.
            The total number of people infected in the population, including the newly infected
            The total number of dead, including those that died during this time step.
        The format of this log should be:
            "Time step {time_step_number} ended, beginning {time_step_number + 1}\n"
        '''
        with open(self.file_name, 'a') as f:
            msg = f"Time step {time_step_number} ended, beginning {time_step_number + 1}\n"
            f.write(msg)
