# Project of Next Generation Networks - Automatic deployment of "containers"

> NOTE: to visualize on VSCode this file press `Ctrl+Shift+V` or `Cmd+Shift+V` on Mac

## Steps to execute the project

1. Open VirtualBox and start comnetsemu
2. Opena a terminal and execute the following command:

```bash
production:
python3 ngn_gui.py #  open the GUI and start controller and mininet

dev:
python3 openShellWithPy.py # open terminal and start controller and mininet
```

3. **(Not necessarly - raccomanded on windows system)** Open a terminal and execute the following command :

```bash
sudo su
```

4. Open a terminal and execute the following command:

```bash
cd /media/sf_shared_NGN_Project
```

5. Open a terminal and execute the following command:

```bash
python3 <file_you_want_to_execute>.py
```

## Description

## Roadmap

1. Isolate traffic between host and server
2. Fixing and improving 

## Requirements

- [x] Creare una repository su GitHub
- [x] Create an SDN network in mininet with multiple switches
- [X] Create a software that is capable of deploying services in the network
  - Services are composed of multiple applications that communicate together to deliver the service (e.g., web server and database)
- [ ] Create a GUI (python recommended) capable of:
  - Deploying service in the network (i.e., starting required applications on existing hosts)
    - Basic idea: choose host depending on usage (e.g., max 2 applications per host)
  - Choose communication requirements for applications
    - E.g., application A needs to communicate with application B
    - Upon choosing requirement, the software automatically configures flows in the switches (keeping track of them, see next point)
  - Stopping applications
    - Upon stopping, remove flows if not required anymore
- [x] Show that applications can actually talk
  - Example of communicating applications are a web server and a database (create fake ones)

![Immage of the final project](./img/Project_SDN.png)
