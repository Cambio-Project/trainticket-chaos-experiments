# Chaos Experiments for TrainTicket
This repository contains the artifacts created during a student research project at the [University of Stuttgart](https://www.uni-stuttgart.de/).
They contain experiments for the TrainTicket benchmark system, partially adapted/ported from work provided by [Martin Straesser](mailto:martin.straesser@uni-wuerzburg.de) at [University of Würzburg](https://www.uni-wuerzburg.de/en/home/).
TrainTicket was developed at the [Fudan University](https://www.fudan.edu.cn/en/) and can be found on [GitHub](https://github.com/FudanSELab/train-ticket).

Specifically, we provide the files used in experiments based on real-world failures in microservice systems, replicated in TrainTicket.
Note that these experiments do not follow the traditional definition of Chaos Engineering, as their goal is to validate the behavior of the system rather than to explore unknown behavior.
Moreover, Chaos Toolkit is used as a tool for fault injection and validation instead of exploration.

In the [`trainticket-fork`](https://github.com/Cambio-Project/trainticket-fork) repository, we provide the branches of TrainTicket that were used in the experiments.
These contain additional files to be used for the fault injection with the Chaos Toolkit.

## Contents

- [`probes/trainticket_probes.py`](probes/trainticket_probes.py) is a Python script with all probes used in the experiments.
- [`results/`](results/) contains all the results gathered when running the experiments.
- [`results/result-visualizations.R`](results/result-visualizations.R) is the script used to analyze the results data, generate the diagrams and a summary of descriptive statistics, written in R.
- The folders [`scenario-one/`](scenario-one/) through [`scenario-five/`](scenario-five/) contain the individual experiments and profiles used in the experiments. A step-by-step explanation on how to run the experiments for replication can be found below.

## Replication
### Requirements
- [Chaos Toolkit](https://chaostoolkit.org/)
- [Pandas](https://pandas.pydata.org/)
- TrainTicket
- [HTTP Load Generator](https://github.com/joakimkistowski/HTTP-Load-Generator) (*)

(*) Please note that, in this work, a newer version of the HTTP load generator was used, which works with profiles in YAML. At the time of writing, this version is not yet published on GitHub.

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


## Further Reading
[Fault Analysis and Debugging of Microservice Systems: Industrial Survey, Benchmark System, and Empirical Study](https://ieeexplore.ieee.org/abstract/document/8580420) - Xiang Zhou, Xin Peng, Tao Xie, Jun Sun, Chao Ji, Wenhai Li, Dan Ding.

[Run-Time Prediction of Power Consumption for Component Deployments](https://ieeexplore.ieee.org/document/8498136) - Jóakim von Kistowski, Maximilian Deffner, Samuel Kounev.

[Modeling and Extracting Load Intensity Profiles](https://dl.acm.org/doi/10.1145/3019596) - Jóakim Von Kistowski, Nikolas Herbst, Samuel Kounev, Henning Groenda, Christian Stier, Sebastian Lehrig
