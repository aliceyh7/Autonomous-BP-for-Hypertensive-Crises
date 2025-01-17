import random
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import math as m
from cmath import pi
from math import floor






#Moving target
def movingTarget():
    global originalTarget
    global movingTargetList
    
    C = originalMAP - originalTarget - 0.001
    r = 0.0055
    
    currentTarget = originalTarget+ C*np.exp(-1*r*absTime) -3
    
    movingTargetList.append(currentTarget)
    return currentTarget


#PID code ########################################################################################################################################################
Kp = .10 #proportional gain
Ki = .8 #integral gain
dt = 1      #change in time 
Kd = .09 #derivative gain

#P component of PID 
def proportional():
    global Kp
    global errorMAP

    correction = max(0, Kp*(errorMAP) )
    
    global PIDpropList
    PIDpropList.append( max(0, errorMAP) )
    
    return correction

#I component of PID
def integral():
    global Ki
    global meanArterialPressure
    global prevError
    global queueError
    global prevIntegral
    global errorMAP
    global loopNum
    
    queueError.append(errorMAP)
    prevIntegral += 1/2*(errorMAP + prevError)/1 # where dt interval is 1
    
    if len(queueError) < sizeQueue:
        loopNum += 1
    
    if len(queueError) >= sizeQueue: #when after 50 loops
        oldestError = queueError.pop(0)
        prevIntegral -= 1/2*(oldestError + queueError[0])/1

        
        # shift queue
        # have a single data point that is the cumulative of the array (reached once array becomes 50)
        # subtract the trapezoid of the first bit in the array, add the trapezoid of the new bit
    


    correction = prevIntegral / loopNum
    
    global PIDintList
    PIDintList.append( max(0, correction) )
    
    return max(0, Ki*correction)


#D component of PID
def derivative():
    global Kd
    global errorMAP
    global prevError
    change =0
    
    if(prevError != 0):
        change = Kd*(errorMAP-prevError)/dt 
    
    global PIDderList
    PIDderList.append( (errorMAP-prevError)/dt  )
    
    prevError = errorMAP
    

    
    return max(0, change)

#PID
def PID():
    global absTime
    absTime +=1
    global PIDList
    global errorMAP
    errorMAP = (meanArterialPressure - movingTarget())/1000
    #print("PID print")
    
    global PIDpropList
    global PIDintList
    global PIDderList
    """
    PIDpropList.append( proportional() )
    PIDintList.append( integral() )
    PIDderList.append( derivative() )
    """
    
    localPID = min(0.1, proportional() + integral() + derivative() )
    
    
    #localPID = ( PIDpropList[-1] + PIDintList[-1] + PIDderList[-1]) 
    
        
    PIDList.append(localPID)
    return localPID

# medicine dissapation code ##################################################################################
def medDissapation(pidReturn):
    # half life = 10 mins (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6675236/)
        
    dissapatedMedicine = pidReturn * (1/2)**(1/600)
    # 0.99884542173 --> reduction in 0.2% per sec
    #print("dissy print")
    return dissapatedMedicine


#resistance code ####################################################################################################################################################

def vesselResistance(med):
    global resistanceList 
    #power function, as found via plotting researched experimental data "transfer.py" by Sourodeep
    
    a = 75.17
    b = -0.9737
        
   
    #print("resistance print")
   
    resistance =  (a * ((5000*med+30.025)** b))
    '''
    if med > 0:
        resistance = 2.793 - med*1000
    else:
        resistance = 2.793
    '''

    '''
    if(med > 60):
        resistance = (a * ((med)** b))
    else:
        resistance = -.023*med + 2.793
    '''

    resistanceList.append(resistance)
 
    return resistance




# windkessel code ####################################################################################################################################################
def windKessel(R):
    global bloodPressureArray
    #Normal Case: even if BP spikes, it will come back down
    #R = 1.05

    #Hypertensive Case: BP rises, and can't come down on its own 
    # R is too high, leading to pressure being too high 
   #R = 1.4

    
    
    #Qh = 370/10
    Qh = 45
    C = 1.18
    dt = 1

    meanArterialPressure = bloodPressureArray[-1]+dt*(Qh/C-bloodPressureArray[-1]/(R*C))

    windyStore.append(meanArterialPressure)
    
    return meanArterialPressure









#Simulation code ##################################################################################################################################################

#function that models patient's tendency to return to high blood pressure
def naturalBodyResist():
    global meanArterialPressure
    if meanArterialPressure < restingHighBP:
        #Change weight once better informed
        meanArterialPressure = meanArterialPressure + bodyResistance*np.random.uniform(0,.25)


#function for increase in patient's blood pressure
def HighSpike(duration, rateOfRise, noiseFreq):
    global pidChangeInBP
    global meanArterialPressure    
    global medInfusionRate
    
    
    for x in range(duration): 
        
            
        #Reflects change in BP from PID's med infusion
        
        
        #updates global meanArterialPressure w/ small addition
        meanArterialPressure = meanArterialPressure + random.random()*rateOfRise
        
        bloodPressureArray.append(meanArterialPressure)
        
        
        pidChangeInBP = windKessel(vesselResistance(medDissapation(PID())))
        meanArterialPressure = pidChangeInBP

        naturalBodyResist()
      
        for x in range(noiseFreq):  
            meanArterialPressure = meanArterialPressure + np.random.uniform(-.2,.2)
            bloodPressureArray.append(meanArterialPressure)

    


#function responsible for creating sustained periods of roughly constant BP in blood pressure profile
def Sustained(duration, noiseFreq): 
   # sustainedNoise = np.random.normal(0,.5,10000)
    global meanArterialPressure
    global absTime
    global pidChangeInBP

    for x in range(duration):
        
        
        pidChangeInBP = windKessel(vesselResistance(medDissapation(PID())))

        #print("BP before pidChange")
        #print(meanArterialPressure)
        meanArterialPressure = pidChangeInBP
        #print("BP after pidChange")
        #print(meanArterialPressure)
        
        bloodPressureArray.append(meanArterialPressure)
        

        naturalBodyResist()
        for x in range(noiseFreq):  
            meanArterialPressure = meanArterialPressure + np.random.uniform(-.2,.2)
            bloodPressureArray.append(meanArterialPressure)
    
    


#function responsible for creating dips in blood pressure profile

def Decrease(duration, rateOfRise, noiseFreq):
    global meanArterialPressure
    global pidChangeInBP
    
    
    for x in range(duration): 
        
        #Reflects change in BP from PID's med infusion
        pidChangeInBP = windKessel(vesselResistance(medDissapation(PID())))
        
        
        #updates global meanArterialPressure w/ small addition
        meanArterialPressure = pidChangeInBP - random.random()*rateOfRise
        
        bloodPressureArray.append(meanArterialPressure)
        
        
        naturalBodyResist()
        
        for x in range(noiseFreq):  
            meanArterialPressure = meanArterialPressure + np.random.uniform(-.2,.2)
            bloodPressureArray.append(meanArterialPressure)

    

#where the profile is created --could possibly use random generator to create random profile#
#############################################################################################

from matplotlib.pyplot import cm
color = iter(cm.rainbow(np.linspace(0, 1, 300)))

   
   
# INPUTS





plt.ion()
fig1, ax1 = plt.subplots(1, 1, num=1, clear=True)
targetMAP = 90
ax1.axhline(y=targetMAP, color ="red", label = 'Target BP = {} mmHg'.format(targetMAP))
ax1.axvline(x=400, color = "blue", label = "Patient faces a high spike at 400 seconds.")
ax1.axvline(x=600, color = "orange", label = "Patient BP naturally trends down at 600 seconds.")


xBP2 = np.arange(1,len(movingTargetList)+1)

for i in np.arange(100,130, .1):
    #sleep(.5)
    #initializing vars 
    bodyResistance = 1.0      #stength of patient's tendency to return to resting high blood pressure 
    restingHighBP = 0.0       #BP patient tends to
    meanArterialPressure =i   #current blood pressure of patient
    targetMAP = 90.0             #desired blood pressure for patient
    errorMAP = 0.0
    bloodPressureArray =[]      #array with all of patient's blood pressure values
    pidChangeInBP = 0.0         #how PID changes the blood pressure
    simulationFlag = False      #indicates if simulation is done running calculation
    pidFlag = True              #indicates if pid is done running calculation
    prevError =0                # error from the previous iteration
    medInfusionRate = 0

    PIDpropList = []
    PIDintList = []
    PIDderList = []
    loopNum = 0
    movingTargetList = []

    sizeQueue = 100              #size of queue with integral errors
    queueError = []               #list of integral errors
    prevIntegral = 0            #integral from previous iteration of PID 

    absTime = 0 # absolute time since start of application


    resistanceList = []
    PIDList =[]

    #user input to set values for a patient
    #meanArterialPressure = float(input("Input patient's current Mean Arterial Blood pressure (MAP for 120/80 is 93)"))
    originalBP = meanArterialPressure
    bloodPressureArray.append(meanArterialPressure)


    """
    meanArterialPressure = float(input("Input patient's current Mean Arterial Blood pressure (MAP for 120/80 is 93)"))
    restingHighBP = float(input("Input patient's current hypertensive resting BP"))
    targetMAP = float(input("Input patient's target Mean Arterial Blood pressure (MAP for 120/80 is 93)"))
    bodyResistance = float(input("How aggressive is the patient's tendency to return to their resting high blood pressure? (1.0-5.0, inclusive)"))
    """

    originalMAP = meanArterialPressure
    originalHighMAP = restingHighBP
    originalTarget = targetMAP
    originalResistance = bodyResistance

    windyStore = [meanArterialPressure]
    
    
    restingHighBP = 150
    
    bodyResistance = 1.5
    meanArterialPressure = i
    print(meanArterialPressure)

    Sustained(400,5)
    HighSpike(200,1.5,5)
    Decrease(400,1.4,5 )
    #Sustained(11000,5)
    
    rainbowColor = next(color)
    
    xBP = np.arange(1, len(bloodPressureArray)+1)/6
    ax1.plot(xBP, bloodPressureArray, color = rainbowColor, linewidth = .5)
    
ax1.set(title="Array of 300 Patients' BP While Being Treated by Autonomous Medication Infusion",
           xlabel="Time (s)", 
           ylabel="Mean Arterial Blood Pressure (mmHg)")
ax1.legend(loc='best')


#############################################################################################


#print("blood pressure readings are: {}".format(bloodPressureArray))
print("resistance values are: {}".format(resistanceList))
#print("PID values are: {}".format(PIDList))

print(windyStore)

print("original patient MAP:{}".format(originalMAP))
print("original patient high Resting MAP:{}".format(restingHighBP))
print("patient target MAP:{}".format(originalTarget))
print("original patient bodyRes:{}".format(originalResistance))



 #%% GRAPHS
plt.ion()
fig1, ax1 = plt.subplots(1, 1, num=1, clear=True)




ax1.plot(xBP2, movingTargetList, color ="grey", label = 'Moving Target')

ax1[0].axhline(y=0, color ="red")
ax1.axhline(y=restingHighBP, color = "purple", label = 'Resting High BP = {}'.format(restingHighBP))
ax1.axhline(y=((restingHighBP+targetMAP)/2), color = "pink" )





ax1.plot(xBP, bloodPressureArray, color = "green", linewidth = .5, label = 'BP          | Initial = {}'.format(originalBP))



ax1.legend(loc='best')

ax1[0].text(650, restingHighBP - 1/5*(restingHighBP-targetMAP), "Hypertensive Tendency: {}".format(bodyResistance))


xPID = np.arange(1, len(PIDList)+1)
ax1[1].axhline(y=0, color = 'grey')

ax1[1].plot(xPID, PIDpropList, color = 'lightblue', label = 'Proportional')
ax1[1].plot(xPID, PIDintList, color = 'green', label = 'Integral')
ax1[1].plot(xPID, PIDderList, color = 'purple', label = 'Derivative')
ax1[1].plot(xPID, PIDList, color = 'black', linewidth = 2, label = 'PID = Drug Infusion Rate')
ax1[1].legend(loc='best')





fig2, ax2 = plt.subplots(1, 2, num=2, clear=True)

xBP = np.arange(1, len(bloodPressureArray)+1)
ax2[0].plot(xBP, bloodPressureArray, color = "green")
ax2[0].axhline(y=targetMAP, color ="red")
ax2[0].axhline(y=0, color ="red")
ax2[0].axhline(y=restingHighBP, color = "purple")
ax2[0].axhline(y=((restingHighBP+targetMAP)/2), color = "pink" )

xPID = np.arange(1, len(PIDList)+1)
ax2[1].axhline(y=0, color = 'grey')
ax2[1].plot(xPID, PIDList, color = 'black')
ax2[1].plot(xPID, PIDpropList, color = 'blue')
ax2[1].plot(xPID, PIDintList, color = 'green')
ax2[1].plot(xPID, PIDderList, color = 'purple')
"""
"""
xPID = np.arange(1, len(bloodPressureArray)+2)
ax1[1].axhline(y=PIDpropList, color = 'green')
ax1[1].axhline(y=PIDintList, color = 'blue')
ax1[1].axhline(y=PIDderList, color = 'purple')
ax1[1].axhline(y=PIDList, color = 'black')

ax1[0].plot(x, yhat, mfc='none', marker='s', markeredgecolor='r', label="Estimates")
ax1[0].plot(xmodel, yhatmodel, color='black', label="Model")
ax1[0].set(
           ylabel="Y", 
           xlabel="X")
ax1[0].legend(loc="best")
ax1[0].grid()

ax1[1].scatter(y, x, color='red', label="Data")
ax1[1].plot(y, xhat, mfc='none', marker='s', markeredgecolor='r', label="Estimates")
ax1[1].plot(ymodel, xhatmodel, color='black', label="Model")
ax1[1].set( 
           ylabel="X", 
           xlabel="Y")
ax1[1].legend(loc="best")
ax1[1].grid()

fig1.set_size_inches(6, 4, forward=True)
fig1.tight_layout()




# %% OLD graphs
#plotting the blood pressure profile (target blood pressure line and line chart of blood pressure values)
x = np.arange(1, len(bloodPressureArray)+1)
y = bloodPressureArray
plt.title("Blood Pressure Sim")
plt.xlabel("Time")
plt.ylabel("Mean Arterial Pressure")
plt.plot(x, y, color ="green")
plt.axhline(y=targetMAP, color ="red")
plt.axhline(y=0, color ="red")
plt.axhline(y=restingHighBP, color = "purple")
plt.axhline(y=((restingHighBP+targetMAP)/2), color = "pink" )




#plt.axvline(x =120)
#plt.axvline(x =240)
#plt.axvline(x =360)
#plt.axvline(x =480)
plt.show()



