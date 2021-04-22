# shellcheck disable=SC2164
cd ../../trainticket-fork/ts-preserve-service/src/main/java/preserve/controller
rm PreserveController.java
cp PreserveController.FAULTY.java PreserveController.java
cd ../../../../../../trainticket-fork/deployment/docker-compose-manifests/
sudo docker-compose -f docker-compose-with-jaeger.yml stop ts-preserve-service
sudo docker-compose -f docker-compose-with-jaeger.yml rm -f ts-preserve-service
sudo docker-compose -f docker-compose-with-jaeger.yml up --build --no-deps --force-recreate -d ts-preserve-service
