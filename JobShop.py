from types import NoneType
import numpy as np
import random
import time
import matplotlib.pyplot as plt


class JobShop:
    # This class i the environment of Job shop problem

    bool_generate_random_jssp = None
    number_job = None
    number_machine = None
    number_features = None

    # the lower limit of one position of job's processing time.
    time_low = None
    # the upper limit of one position of job's processing time.
    time_high = None

    # Matrix of processing time, M_processing_time[i,j] is the processing time of job i's position j.
    M_processing_time = None
    # Matrix of processing time, M_processing_order[i,j] is the machine restrain of job i's position j.
    M_processing_order = None
    M_start_time = None
    M_end_time = None
    X_schedule_plan = None
    schedule_line = None

    def __init__(self,number_machine,number_job,time_low,time_high,bool_random):
        self.number_job = number_job
        self.bool_generate_random_jssp = random
        self.number_machine = number_machine
        self.time_low = time_low
        self.time_high = time_high
        self.schedule_line = []
        self.GenerateRandomProblem()

    def Get_Possible_Job_Position(self):
        # ergodic the schedule_line, and return the possible position to produce of jobs
        #  <- not understood
        
        job_position_list = [0 for i in range(self.number_job)]
        for job_id, job_position in self.schedule_line:
            if job_position < self.number_machine-1:
                job_position_list[job_id] = job_position+1
            else:
                job_position_list[job_id] = -1

        return [[i,job_position_list[i]] for i in range(len(job_position_list))]

    def Get_Features(self, possible_job_position):
        # return the features of current state

        featrues = []
        for job_id, job_position in possible_job_position:
            f_item = self.GetFeature(job_id,job_position)
            featrues.append(f_item)

        return featrues

    def Step(self,action=None):
        # be called in main function
        # input action and return state score and done
        # action: choose a job ot process
        # state

        done = False
        if action == None:
            self.MeasurementAction(self.schedule_line)
            possible_pob_position = self.Get_Possible_Job_Position()
            state = np.array(self.Get_Features(possible_pob_position))
            score = 0

        else:
            job_position_list = [0 for i in range(self.number_job)]
            for job_id,job_position in self.schedule_line:
                if job_position < self.number_machine-1:
                    job_position_list[job_id] = job_position + 1
                else:
                    job_position_list[job_id] = -1
            if job_position_list[action] == -1:
                done = True
                canchoose = [[i, job_position_list[i]] for i in range(
                                    self.number_job) if job_position[i] != -1]
                action = canchoose[0]
            else:
                action = [action, job_position_list[action]]
            
            self.schedule_line.append(action)
            self.MeasurementAction(self.schedule_line)
            # self.PlotResult()
            score = np.max(self.M_end_time)

            possible_pob_position = self.Get_Possible_Job_Position()
            state = np.array(self.Get_Features(possible_pob_position))

        state = [np.reshape(state[i], (1,2,)) for i in range(self.number_job)]

        return state, score, done


