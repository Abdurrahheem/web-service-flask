from joblib import dump, load
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
import numpy as np 

np.random.seed(0)
iris_X, iris_y = datasets.load_iris(return_X_y=True)
indices = np.random.permutation(len(iris_X))
iris_X_train = iris_X[indices[:-10]]
iris_y_train = iris_y[indices[:-10]]
iris_X_test = iris_X[indices[-10:]]
iris_y_test = iris_y[indices[-10:]]

# Create and fit a nearest-neighbor classifier
knn = KNeighborsClassifier()
knn.fit(iris_X_train, iris_y_train)

dump(knn, 'irismodel.joblib') 