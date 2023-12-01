import parameterImportance as pi

from statistics import pvariance

# also import the input data from main when that code is made

#for now, use list from here, but should be from inputted values
inputs = [7,2,2,2,2,2,2,2,2]

#ph: 7,Hardness: 0,Solids: <500,Chloramines: <4,Sulfate: <250,Conductivity: <400,Organic_carbon: <25,Trihalomethanes: <80,Turbidity: <5,
#conductivity: uS/cm , turbitity: NTU, solids: mg/L, hardness: mg/L, organiz_carbon: mg/L, Trihalomethanes: mg/L, 
perfectPara = [7,1,1,4,250,400,25,1,0.1]
maxPara = [6, 500, 500,100, 10000, 1000, 100,100,5]
adjPara = []

#calculate value value /100 of each parameter. Uses deviation multiplied by importance found 
continue_loop = True


for i in range(len(perfectPara)):
    #if i is on pH
    if i==0 and inputs[i]>6 and inputs[i]<8:
        adjPara.append(100-(((inputs[i]-perfectPara[i]))/perfectPara[i])*100)
    elif i==0 and inputs[0]<6 or inputs[0]>8:
        print('Ph out of allowable range\n')
        adjPara=[0,0,0,0,0,0,0,0,0]
        continue_loop = False
        break
    else:
        #if input is between ideal and max limit. Finds percent to be subtracted     
        if inputs[i]>perfectPara[i] and inputs[i]<maxPara[i] and continue_loop==True:
            adjPara.append(100-((inputs[i]/(maxPara[i]-perfectPara[i])*100)))
        #if input better than ideal. Considering still ideal
        elif inputs[i]<perfectPara[i] and i!=0 and continue_loop==True:
            adjPara.append(100)
        #if input worse than max limit. Auto 0
        elif inputs[i]>maxPara[i]:
            print('A parameter is out of the maximum allowable value for its parameter\n')
            adjPara=[0,0,0,0,0,0,0,0,0]
            break


print(adjPara)
print(pi.importance)
#importance times the deviation to give result /100
pctAdjPara = adjPara*pi.importance

respct = sum(pctAdjPara)
#print(pctAdjPara)
print (respct)

#scores for potable vs not divide around 68-72. Below is not potable, above is potable
if respct<68:
    print("We recommend you do not drink this water. Below are recommendations based on your entries:\n\n")
elif respct>68 and respct<72:
    print("Based off of your entries, this water is on the verge of being unsafe for drinking. Use caution. Below are recommendations to ensure it is drinkable:\n\n")
elif respct>72 and respct<85:
    print("This water is safe for drinking. To improve quality, consider the steps below:\n\n")
elif respct>85 and respct<100:
    print("This water is very safe to drink! Enjoy!")
else:
    print("Error in grading scale")

#if statements for above and below for parameters (alex)
