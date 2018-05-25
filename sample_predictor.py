#Import Library of Gaussian Naive Bayes model
from sklearn.naive_bayes import GaussianNB
import numpy as np

#assigning predictor and target variables
# x is the input, y is the output: Input [-3, 7] gives 3
'''
To make this about football scores, 
each x array would be a list of variables that decided the match like form, head-to-head, ranking, team value and stuff
the values in x lists should not be correlated like using fifa ranking and a different ranking together would make ranking be counted twice
each y value would be either 0, 1, 2 depending on the result
'''
x= np.array([[-3,7],[1,5], [1,2], [-2,0], [2,3], [-4,0], [-1,1], [1,1], [-2,2], [2,7], [-4,1], [-2,7]])
y = np.array([3, 3, 3, 3, 4, 3, 3, 4, 3, 4, 4, 4])

#Create a Gaussian Classifier
model = GaussianNB()

# Train the model using the training sets 
model.fit(x, y)

#Predict Output 
predicted= model.predict([[1,2],[3,4]]) # Can predict multiple values at one time. model.predict([1,2]) would output one prediction
print (predicted)

