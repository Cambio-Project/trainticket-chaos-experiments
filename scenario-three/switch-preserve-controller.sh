# shellcheck disable=SC2164
cd ../../trainticket-fork/ts-preserve-service/target
rm ts-preserve-service-1.0.jar
cp ts-preserve-service-1.0.FAULTY ts-preserve-service-1.0.jar
cd ../../../../../../deployment/docker-compose-manifests/
sudo docker-compose -f docker-compose-with-jaeger.yml stop ts-preserve-service
sudo docker-compose -f docker-compose-with-jaeger.yml rm -f ts-preserve-service
sudo docker-compose -f docker-compose-with-jaeger.yml up --build --no-deps --force-recreate -d ts-preserve-service
