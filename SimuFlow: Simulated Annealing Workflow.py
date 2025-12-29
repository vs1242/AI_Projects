import random
import math
##
Jobs = [(3,6), (10,1), (3,2), (2,4), (8,8)]
J=5 
M=2
N=2
current_job_sched= [4, 1, 5, 3, 2]

def SA(current_job_sched, Jobs):
    T = 1000
    #current_job_sched = random.permutation(J)
    current_opt_sched=allocate_ops_to_machines(current_job_sched,N,M)
    
    for i in range(400):
        next_job_sched=successor(current_job_sched,N)
        #print(next_job_sched)
        next_opt_sched=allocate_ops_to_machines(next_job_sched,N,M)
        deltaE=comp_makespan(next_opt_sched)- comp_makespan(current_opt_sched)
        print(f"delta E is: {deltaE}")
        if deltaE>0:
            current_job_sched = next_job_sched
        else:
            r = random.uniform(0,1)
            if (math.exp(deltaE/T) <= r):
                current_job_sched = next_job_sched
                current_opt_sched = next_opt_sched
        T = T*0.99
    return comp_makespan(current_opt_sched)

def successor(current_job_sched, N):
    index1 = random.randint(0, len(current_job_sched) - 1)
    index2 = random.randint(0, len(current_job_sched) - 1)
    
    # Ensure the indices are distinct
    while index2 == index1:
        index2 = random.randint(0, len(current_job_sched) - 1)
    
    # Swap the elements at the chosen indices
    current_job_sched[index1], current_job_sched[index2] = current_job_sched[index2], current_job_sched[index1]

    return current_job_sched

def allocate_ops_to_machines(current_job_sched, N, M):
    opt_sched=[] #This is a list that will have an operation schedule 
    #assuming M = number of operations

    machine_index = 1 #a parameter that stores the index of the current machine
    free_time = [0 for _ in range(M)]
    #for i in M: #”machines” will be equal to the number of machines
        #free_time[i] = 0 #a parameter that stores the time at which a machine finishes its previous job and gets free; free time of all machines is set to 0 initially

    for job in current_job_sched:

        start_time = 0
        end_time = 0 #parameters to record the start and end times of each job operation; initially set to 0 for every job

        for opt in range(N): #operation will be used as an iterator to iterate through M
            #print(f"machine index: {machine_index} and N: {N}")
            start_time = max(free_time[machine_index-1], end_time) #start time will be based on larger value between free_time array and end time
            #print(f"job = {job}, opt= {opt}")
            end_time = start_time + Jobs[job-1][opt-1] #end time will be equal to start time + time taken to run current operation
            free_time[machine_index-1] = end_time #now end time will be assigned to free_time of the current machine
            opt_sched.append([opt, start_time, end_time, machine_index])
            #Append opt_sched list with(current job operation number, start_time, end_time, machine_index) // opt_shedule list will be updated
            
            machine_index += 1 #Increment machine_index by 1 // increment machine index
            if machine_index > M: #// if machine index is greater   than number of machines then it will be reset to 1 
                machine_index = 1

    return opt_sched #//return the operations schedule list

def comp_makespan(opt_sched):

    m_span=0 #// initially assigning m_span=0 

    for opt in opt_sched: #//this loop will now enumerate through starting time, end time of opt_sched 
        current_end=opt[2] #// it will take store ending time into current_end
        m_span=max(m_span, current_end) #//m_span will be updated 

    return m_span

makespan = SA(current_job_sched, Jobs)
print("Final makespan is :", makespan)
