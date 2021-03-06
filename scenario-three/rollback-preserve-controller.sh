# shellcheck disable=SC2164
cd /home/elcpt/Documents/train-ticket/ts-preserve-service/target
rm ts-preserve-service-1.0.jar
cp ts-preserve-service-1.0.SAFE ts-preserve-service-1.0.jar
cd /home/elcpt/Documents/train-ticket/deployment/docker-compose-manifests/
sudo docker-compose -f docker-compose-with-jaeger.yml stop ts-preserve-service
sudo docker-compose -f docker-compose-with-jaeger.yml rm -f ts-preserve-service
sudo docker-compose -f docker-compose-with-jaeger.yml up --build --no-deps --force-recreate -d ts-preserve-service
