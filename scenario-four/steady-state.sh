#!/bin/bash
java -jar "../loadgenerator/httploadgenerator.jar" loadgenerator &
sleep 3s
java -jar "../loadgenerator/httploadgenerator.jar" director --load steady-state-load.csv -o steady-log.csv --yaml steady-state-profile.yaml
echo "Finished steady state load generating run."