# Handoff Simulator
## Introduction
- A simple simulator used four different handoff policies.
    - Best policy:
    ```
    New Power > Old Power
    ```
    - Threshold policy: (T = -110 dBm)
    ```
    New Power > Old Power && Old Power < T
    ```
    - Entropy policy: (E = +5 dBm)
    ```
    New Power > Old Power + E
    ```
    - Self-defined policy: (multiplier = 0.9, Minimum Power = -125 dBm) 
    ```
    New Power > Old Power * multiplier && New Power > Minimum Power
    ```
![](https://i.imgur.com/ljjlvxL.png)
- Each point represents a car. Use Poisson Distribution to assume that there are 2 cars/min entering to this zone. The simulation time is for one day(=86400 seconds).
- When a car meet the intersection, there are different possibilities to different directions.
    - Straight: $\frac{1}{2}$
    - Right: $\frac{1}{3}$
    - Left: $\frac{1}{6}$
## Result
- To watch the simulation for 86400 seconds, run:
```shell
python simulator.py
```
- To plot policy comparison figure and print the result, run:
```shell
python main.py
```
> It may cost 10~20 minutes to plot the figure and print the result.
- Policy comparison figure
![](https://i.imgur.com/l4WMYtV.png)
- Result in the console
![](https://i.imgur.com/N7UCexM.png)