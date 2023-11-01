import pandas as pd
import sklearn
from matplotlib import pyplot
from sklearn.ensemble import RandomForestClassifier

# Load logan's dataset
data = pd.read_csv("water_potability.csv")

# take out all null rows, could be changed later but this seems the most accurate
data_clean = data.dropna()

#check for pH levels outside of 6.5 and 7.5
condition = (data['ph']<6.5)|(data['ph']>8.5)



#split data into parameters and result
x = data_clean[['ph','Hardness','Solids','Chloramines','Sulfate','Conductivity','Organic_carbon','Trihalomethanes','Turbidity']]
y = data_clean['Potability']


#make model
model = RandomForestClassifier()
model.fit(x,y)

#get importance
importance = model.feature_importances_
print(importance)
#prints importance
features = ['ph','Hardness','Solids','Chloramines','Sulfate','Conductivity','Organic_carbon','Trihalomethanes','Turbidity']
for i,v in enumerate(importance):
    print('Feature: %s, Score: %.5f' % (features[i],v))


#create pie chart
sizes = importance*100
pyplot.pie(sizes,labels=features,autopct='%1.1f%%',startangle=140)
pyplot.title('Parameter Affect on Potability')
pyplot.show()



#final csv
data_clean.to_csv('cleaned_data.csv',index=False)