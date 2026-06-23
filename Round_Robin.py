import tkinter as tk # Used for GUI creation
import pandas as pd # Used for table creation and better visualisation

def Round_Robin(processes, quantum):
    n = len(processes)
    remaining_time = [] # Creates a list to store the remaining burst time for each process
    for p in processes: 
      remaining_time.append(p['burst_time']) # Adds the burst time of each to the list without overwriting previous data
    time = 0 # Current/initial time
    gantt = [] # For Gantt chart representation and the result is given as (process_id, completion_time); ordered by which one finishes first

    while True:
        done = True
        all_waiting = True # Used to check if all processes are waiting and none are executing; if true, it means that the CPU is idle and we can skip the time increment
        for i in range(n):
            if remaining_time[i] > 0:
                done = False
            
                if processes[i]['arrival_time'] > time: # If the arrival time of the process is greater than the current time, it means that the process has not arrived yet and we can skip it
                    continue # Skip to the next process in the loop
                
                all_waiting = False
                
                if remaining_time[i] > quantum:
                    time += quantum
                    remaining_time[i] -= quantum
                    gantt.append((processes[i]['process_id'], time))
                else:
                    time += remaining_time[i]
                    processes[i]['completion_time'] = time
                    remaining_time[i] = 0
                    gantt.append((processes[i]['process_id'], time))
        if done:
            break
        
        if all_waiting:
            future_arrivals = [
                processes[i]['arrival_time']
                for i in range(n)
                if remaining_time[i] > 0
                and processes[i]['arrival_time'] > time
            ]

            if future_arrivals:
                time = min(future_arrivals)
            continue  

    for p in processes:
        p['turnaround_time'] = p['completion_time'] - p['arrival_time']  # TAT = Completion - Arrival
        p['waiting_time'] = p['turnaround_time'] - p['burst_time']       # WT  = TAT - Burst

    return processes, gantt

# User input for num of processes(n), arrival time, burst time, and time quantum
n = int(input("Enter the number of processes: "))
processes = [] # Creates a list to store process information
for i in range(n):
    try: # Error handling
     print(f"Process {i+1}: ") # Process numbering and i+1 iterates each time the loop runs; for total number of processes(n)
     arrival = int(input(f"Enter the arrival time for process {i+1}: ")) # User input for arrival time of each process
     burst = int(input(f"Enter the burst time for process {i+1}: ")) # User input for burst time of each process
     if burst < 0: # Error handling for negative burst time
        print("Invalid input. Do not enter negative numbers. Enter a positive integer for the burst time.")
     elif arrival < 0:  # Error handling for negative arrival time
        # Need to add error handling for a.t > tot(b.t)
        print("Invalid input. Do not enter negative numbers. Enter a positive integer for the arrival time.")
     else:
         processes.append({'process_id': i+1, 'burst_time': burst, 'arrival_time': arrival}) # Adds the info into the dictionary and appends it instead of overwriting
    except ValueError: # Error handling for non-integer input
        print("Invalid input. Do not enter alphabets. Enter a positive integer for the burst time.")

try:
    quant = int(input("Enter the time quantum: ")) # User input for time quanta
    quantum = quant # Assigns quant to variable quantum for use in the Round Robin function
    if quant < 0: # Error handling
        print("Invalid input. Do not enter negative numbers. Enter a positive integer for the time quantum.")
except ValueError: # Error handling for non-integer input
    print("Invalid input. Do not enter alphabets. Enter a positive integer for the time quantum.")
    
# Calls the Round Robin function and stores the result in a variable

result, gantt = Round_Robin(processes, quantum)
df = pd.DataFrame(result) # Creates a DataFrame from the result for better visualization
df = df[['process_id', 'arrival_time', 'burst_time', 'completion_time', 'turnaround_time', 'waiting_time']] # Reorders the columns for better readability

# Drops all the values into a table format

print("\n--- Round Robin Scheduling ---") # Header for the table
 # The .to_markdown function is used to print the DataFrame in a table format with the fancy_grid style
print(df.to_markdown(index=False, tablefmt="fancy_grid")) # The index=False is used to remove the index column from the table


# Calculate the averages and prints them

avg_tat = df['turnaround_time'].mean() # Used the .mean function as it is more efficient than calculating the sum and dividing by the length of the list
avg_wt  = df['waiting_time'].mean() # The same as above but for waiting time
print(f"\nAverage Turnaround Time : {avg_tat:.2f}")  # Prints to 2d.p due to the (.2f) format specifier
print(f"Average Waiting Time    : {avg_wt:.2f}") # Prints to 2d.p due to the (.2f) format specifier

# Prints the process information after scheduling
print(f"\nGantt Chart: {gantt}")


#def main():
 #  root.geometry("800x600")
  #  root.title("Round Robin Scheduling")

 #   root.mainloop()



