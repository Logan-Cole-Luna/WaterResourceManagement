import parameterImportance as pi

from statistics import pvariance

# also import the input data from main when that code is made

#for now, use list from here, but should be from main



inputs = [7.5,200,000,000,0000,000,000,0000,000]

#ph: 7,Hardness: 0,Solids: unknown,Chloramines: <4,Sulfate: <250,Conductivity: <400,Organic_carbon: <25,Trihalomethanes: <80,Turbidity: <5,Potability
perfectPara = [7,1,1,4,250,400,25,80,5]
adjPara = []

#calculate value value /100 of each parameter. Uses deviation multiplied by importance found 

for i in range(len(perfectPara)):
    adjPara.append(100-(((abs(inputs[i]-perfectPara[i]))/perfectPara[i])*100))

#importance times the deviation to give result /100
pctAdjPara = adjPara*pi.importance

print (pctAdjPara)

#determine score for great, good, decent, could be better, and horrible water\

#if statements for above and below for parameters
