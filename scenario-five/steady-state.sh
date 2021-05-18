#!/bin/bash
# Steady state file for scenario 5
echo "Starting loadgenerator in background"
java -jar "../loadgenerator/httploadgenerator.jar" loadgenerator &
sleep 3s
java -jar "../loadgenerator/httploadgenerator.jar" director --load steady-state-load.csv -o /dev/null --yaml steady-state-profile.yaml > /dev/null &
echo "Finished launching load generation, returning to experiment"