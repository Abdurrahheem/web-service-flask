import numpy as np
from sklearn import datasets
from flask import Flask
from markupsafe import escape
from sklearn.neighbors import KNeighborsClassifier

app = Flask(__name__)

@app.route('/')
def hello_world():
    print(f'This is {3}')
    return '<h1 style="text-align:center"> Hello, my best frined! <br/> How is the day? </h1>'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f"squared: {escape(float(username)**2)}"

@app.route('/avg/<array>')
def avg(array):
    # avarage of an array
    array = array.split(',')
    array = [float(s) for s in array]
    return f'<h1 style="text-align:center"> The avarage of your array   \
     is {str(sum(array)/len(array))} </h1>'

@app.route('/iris/<data>')
def iris(data):
    data = data.split(',')
    data = [float(s) for s in data]
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
    result = str(knn.predict(np.array(data).reshape(1,-1)).item(0))

    return '<h2>Your Iris flawer is {}</h2>'.format(result)