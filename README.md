## trainticket-chaos-experiments
Chaos experiments based on real-life incidents, for the TrainTicket benchmark system

### Requirements
- Chaos Toolkit
- Pandas
- TrainTicket benchmark system
- httploadgenerator new version 

### Preparations
In order to run these experiments, the folder containing the custom probes and actions has to be added to the `PYTHONPATH` environment variable as follows:
#### Adding the probe file to the PYTHONPATH
Execute the following command with the appropriate path in place of the placeholder:
```shell
export PYTHONPATH="/<path>/trainticket-chaos-experiments/probes:$PYTHONPATH"
```
Furthermore, please ensure that the following two conditions are met:
1. The TrainTicket microservice benchmark system is running and reachable at `http://localhost:8080`.
2. A `loadgenerator` directory that contains the loadgenerator JAR exists as a subdirectory of the repository root

### Run experiments
In order to run chaos experiments, simply enter a scenario's folder and execute the following:
```shell
chaos run experiment.json
```
