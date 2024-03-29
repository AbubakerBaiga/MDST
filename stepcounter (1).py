
import numpy as np
import matplotlib.pyplot as plt

#Simple function to visualize 4 arrays that are given to it
def visualize_data(timestamps, x_arr,y_arr,z_arr,s_arr):
  #Plotting accelerometer readings
  plt.figure(1)
  plt.plot(timestamps, x_arr, color = "blue",linewidth=1.0)
  plt.plot(timestamps, y_arr, color = "red",linewidth=1.0)
  plt.plot(timestamps, z_arr, color = "green",linewidth=1.0)
  plt.show()

  #magnitude array calculation
  m_arr = []
  for i, x in enumerate(x_arr):
    m_arr.append(magnitude(x_arr[i],y_arr[i],z_arr[i]))
  plt.figure(2)

  #plotting magnitude and steps
  plt.plot(timestamps, s_arr, color = "black",linewidth=1.0)
  plt.plot(timestamps, m_arr, color = "red",linewidth=1.0)
  plt.show()


#Function to read the data from the log file
#TODO Read the measurements into array variables and return them
def read_data(out):
    timestamps = []
    x_array = []
    y_array = []
    z_array = []
    #TODO implementation
    #CSV file has no headers, we can access columns by index
    csv_array = np.genfromtxt(out, delimiter=',')
    timestamps = csv_array[:, 0]
    x_array = csv_array[:, 1]
    y_array = csv_array[:, 2]
    z_array = csv_array[:, 3]
   
    return timestamps, x_array, y_array, z_array
    #return [0],[0],[0],[0]

#Function to count steps.
#Should return an array of timestamps from when steps were detected
#Each value in this arrray should represent the time that step was made.
def count_steps(timestamps, x_arr, y_arr, z_arr, threshold=16.9):
    step_counts = []
    for i in range(1, len(timestamps) - 1):
        # Calculate the magnitude of acceleration at each timestamp
        mag = magnitude(x_arr[i], y_arr[i], z_arr[i])

        # Check if the magnitude exceeds the threshold and is a peak
        if mag > threshold and mag > magnitude(x_arr[i - 1], y_arr[i - 1], z_arr[i - 1]) and mag > magnitude(x_arr[i + 1], y_arr[i + 1], z_arr[i + 1]):
            step_counts.append(timestamps[i])

    return step_counts

#Calculate the magnitude of the given vector
def magnitude(x,y,z):
  return np.linalg.norm((x,y,z))

#Function to convert array of times where steps happened into array to give into graph visualization
#Takes timestamp-array and array of times that step was detected as an input
#Returns an array where each entry is either zero if corresponding timestamp has no step detected or 50000 if the step was detected
def generate_step_array(timestamps, step_time):
  s_arr = []
  ctr = 0
  for i, time in enumerate(timestamps):
    if(ctr<len(step_time) and step_time[ctr]<=time):
      ctr += 1
      s_arr.append( 30 )
    else:
      s_arr.append( 0 )
  while(len(s_arr)<len(timestamps)):
    s_arr.append(0)
  return s_arr

#Check that the sizes of arrays match
def check_data(t,x,y,z):
  if( len(t)!=len(x) or len(y)!=len(z) or len(x)!=len(y) ):
    print("Arrays of incorrect length")
    return False
  print("The amount of data read from accelerometer is "+str(len(t))+" entries")
  return True

def main():
      #read data from a measurement file, change the inoput file name if needed
  timestamps, x_array, y_array, z_array = read_data("out.csv")
  #Chek that the data does not produce errors
  if(not check_data(timestamps, x_array,y_array,z_array)):
    return
  #Count the steps based on array of measurements from accelerometer
  st = count_steps(timestamps, x_array, y_array, z_array)
  #Print the result
  print("This data contains "+str(len(st))+" steps according to current algorithm")
  #convert array of step times into graph-compatible format
  s_array = generate_step_array(timestamps, st)
  #visualize data and steps
  visualize_data(timestamps, x_array,y_array,z_array,s_array)

main()

