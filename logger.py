import os
from person import Person
from virus import Virus


class Logger(object):
    ''' Utility class responsible for logging all interactions during the simulation. '''

    def __init__(self, file_name):
        self.file_name = file_name

    def write_metadata(self, *args):
        '''
        The simulation class should use this method immediately to log the specific
        parameters of the simulation as the first line of the file.
        '''
        with open(self.file_name, 'w') as f:
            msg = f'Population Size: {args[0]}    Vaccination Percentage: {args[1]}    Virus: {args[2]}    Mortality Rate: {args[3]}    Basic Reproduction Number: {args[4]}\n'
            f.write(msg)

    def log_interaction(self, *args, random_person_sick=None,
                        random_person_vacc=None, did_infect=None):
        '''
        The Simulation object should use this method to log every interaction
        a sick person has during each time step.
        '''
        with open(self.file_name, 'a') as f:
            if did_infect and not random_person_vacc and not random_person_sick:
                msg = f"{args[0]._id} infects {args[1]._id}.\n"
                f.write(msg)
            elif not did_infect:
                if random_person_vacc:
                    msg = f"{args[0]._id} didn't infect {args[1]._id} because they are already vaccinated.\n"
                    f.write(msg)
                elif random_person_sick:
                    msg = f"{args[0]._id} didn't infect {args[1]._id} because they are already sick.\n"
                    f.write(msg)
                else:
                    msg = f"{args[0]._id} didn't infect {args[1]._id} because they resisted the virus.\n"
                    f.write(msg)

    def log_infection_survival(self, *args):
        ''' The Simulation object uses this method to log the results of every
        call of a Person object's .did_survive_infection() method.
        The format of the log should be:
            "{person.ID} died from infection\n" or "{person.ID} survived infection.\n"
        '''
        with open(self.file_name, 'a') as f:
            if args[1]:
                msg = f"{args[0]._id} survived infection.\n"
                f.write(msg)
            elif not args[1]:
                msg = f"{args[0]._id} died from infection.\n"
                f.write(msg)

    def log_time_step(self, *args):
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
            msg = f"Time step {args[0]} ended, beginning {args[0] + 1}\n"
            f.write(msg)
