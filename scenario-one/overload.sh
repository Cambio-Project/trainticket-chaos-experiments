#!/bin/bash
java -jar "../loadgenerator/httploadgenerator.jar" loadgenerator &
sleep 3s
java -jar "../loadgenerator/httploadgenerator.jar" director --load overload.csv -o overload-log.csv --yaml overload-foodservice-profile.yaml
echo "Finished overloading run."