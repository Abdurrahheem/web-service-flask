docker exec -it flask-hello_flask_1 bash

docker exec -it flask-hello_flask_1 python train_model.py

curl --header "Content-Type: application/json" \
--request POST \
--data '{"flower":"2,4,5,7"}' \
http://localhost:5000/iris_post