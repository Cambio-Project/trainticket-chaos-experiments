# shellcheck disable=SC2164
cd /home/elcpt/Documents/train-ticket/ts-inside-payment-mongo/
rm auth-config-current.js
cp auth-config-bad.js auth-config-current.js
cd /home/elcpt/Documents/train-ticket/deployment/docker-compose-manifests/
sudo docker-compose -f docker-compose-with-jaeger.yml stop ts-inside-payment-mongo
sudo docker-compose -f docker-compose-with-jaeger.yml rm -f ts-inside-payment-mongo
sudo docker-compose -f docker-compose-with-jaeger.yml up --build --no-deps --force-recreate -d ts-inside-payment-mongo
