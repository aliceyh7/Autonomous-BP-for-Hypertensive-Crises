import random
from time import sleep
import numpy as np
import matplotlib.pyplot as plt

#initializing two variables related to patient
bodyResistance = 1.0
restingHighBP = 0.0
meanArterialPressure =0.0
targetBloodPressure = 0.0
bloodPressureQueue =[]
pidChangeInBP = 0.0
simulationFlag = False
pidFlag = True


#user inputs desired values into two previously initialized values
meanArterialPressure = float(input("Input patient's current Mean Arterial Blood pressure (MAP for 120/80 is 93)"))
targetBloodPressure = float(input("Input patient's target Mean Arterial Blood pressure (MAP for 120/80 is 93)"))
restingBP = float(input("Input patient's current hypertensive resting BP"))

def naturalBodyResist():
    global meanArterialPressure
    if meanArterialPressure < restingBP:
        #Change weight once better informed
        meanArterialPressure = meanArterialPressure + bodyResistance*np.random.uniform(0,.25)

 #full function with no noise

def HighSpike(duration, rateOfRise, noiseFreq):
    
    #pidFlag = True
    for x in range(duration): 
        if pidFlag == True:
           # pidFlag = False
            
            #Reflects change in BP from PID's med infusion
            global meanArterialPressure
            global pidChangeInBP
            meanArterialPressure = meanArterialPressure + pidChangeInBP
            pidChangeInBP =0
            
            #updates global meanArterialPressure w/ small addition
            meanArterialPressure = meanArterialPressure + random.random()*rateOfRise
            
            bloodPressureQueue.append(meanArterialPressure)
            simulationflag = True
            # run PID
            #   set sim flag to false, 
            #   use meanArterialPressure as actualMAP; 
            #   calculate med infusion, converted through transfer function through resistance 
            #   Updates pidChangeInBP 
            #   set pid flag to true
        naturalBodyResist()
      
        for x in range(noiseFreq):  
            meanArterialPressure = meanArterialPressure + np.random.uniform(-.2,.2)
            bloodPressureQueue.append(meanArterialPressure)

    #pidFlag = False

        
#function responsible for creating sustained periods of roughly constant BP in blood pressure profile
def Sustained(duration, noiseFreq): 
    sustainedNoise = np.random.normal(0,.5,10000)
    pidFlag = True
    for x in range(duration):
        if pidFlag == True:
            pidFlag = False
            global meanArterialPressure
            meanArterialPressure = meanArterialPressure + pidChangeInBP
            bloodPressureQueue.append(meanArterialPressure)
            simulationflag = True
            # set sim flag to false
            # run PID on meanArterialPressure as actualMAP
            #   calculate  med infusion, converted through transfer function through resistance 
            #   Updates pidChangeInBP 
            #   set pid flag to true
        naturalBodyResist()
        for x in range(noiseFreq):  
            meanArterialPressure = meanArterialPressure + np.random.uniform(-.2,.2)
            bloodPressureQueue.append(meanArterialPressure)
    
    #pidFlag = False

#function responsible for creating dips in blood pressure profile

def Decrease(duration, rateOfRise, noiseFreq):
    pidFlag = True
    for x in range(duration): 
        if pidFlag == True:
            #pidFlag = False
            global meanArterialPressure
            global pidChangeInBP
            #Reflects change in BP from PID's med infusion
            meanArterialPressure = meanArterialPressure + pidChangeInBP
            pidChangeInBP =0
            
            #updates global meanArterialPressure w/ small addition
            meanArterialPressure = meanArterialPressure - random.random()*rateOfRise
            
            bloodPressureQueue.append(meanArterialPressure)
            simulationflag = True
            # run PID
            #   set sim flag to false, 
            #   use meanArterialPressure as actualMAP; 
            #   calculate med infusion, converted through transfer function through resistance 
            #   Updates pidChangeInBP 
            #   set pid flag to true
        naturalBodyResist()
        
        for x in range(noiseFreq):  
            meanArterialPressure = meanArterialPressure + np.random.uniform(-.2,.2)
            bloodPressureQueue.append(meanArterialPressure)

    #pidFlag = False


#where the profile is created --could possibly use random generator to create random profile#
#############################################################################################

Decrease(20 ,2,5)
Sustained(20,5)
HighSpike(20,2, 5)
Sustained(20,5)


#############################################################################################

for x in bloodPressureQueue: 
    print(x)

print("blood pressure readings are: {}".format(bloodPressureQueue))


 
#plotting the blood pressure profile (target blood pressure line and line chart of blood pressure values)
x = np.arange(1, len(bloodPressureQueue)+1)
y = bloodPressureQueue
plt.title("Blood Pressure Sim")
plt.xlabel("Time")
plt.ylabel("Mean Arterial Pressure")
plt.plot(x, y, color ="green")
plt.axhline(y=targetBloodPressure, color ="red")
plt.axvline(x =120)
plt.axvline(x =240)
plt.axvline(x =360)
plt.axvline(x =480)
plt.show()



