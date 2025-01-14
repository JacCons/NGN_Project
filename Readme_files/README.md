# Next Generation Networks Project - Automatic deployment of "containers" - Berardo C., Castagnaro T., Consolaro J.

> NOTE: to visualize this file on VSCode press `Ctrl+Shift+V` or `Cmd+Shift+V` on Mac

## INTRODUCTION
This project integrates Software-Defined Networking (SDN) with Mininet to dynamically deploy and manage services composed of interconnected applications. A Python-based GUI simplifies interaction and management.

### Key Features

- SDN Network: Simulated multi-switch network in Mininet with centralized flow control via an SDN controller.
- Service Deployment: Deploy and manage multi-application services with automated host selection and flow configuration.
- GUI: Intuitive interface for deploying services, managing flows, and monitoring network activity.
- Dynamic Flow Management: Automatically configure and clean up network flows based on application requirements.

## PREREQUISITES
- Install virtualbox and the Comnetsemu Virtual Machine
- Add NGN_Project as a shared folder in Comnetsemu VM settings. 
  Run the following command to access the shared folder with privileges:
    ```bash
      sudo usermod -aG vboxsf vagrant
    ```
- For Mac users : install XQuartz and [enable forwarding](X11_setup.md)
- For Windows users: install mobaXterm and [enable forwarding](X11_setup.md)
- Install [Python 3.7](Install_Python.md) version on the VIrtual Machine

## HOW TO RUN THE APPLICATION

1. Open VirtualBox and start Comnetsemu Virtual Machine
2. After logging-in, for a better “manageability”, instead of running commands directly into the VM it might be worth to use your own terminal and ssh into the VM. To do so, run:
    ```bash
      ssh -X -p 2222 vagrant@localhost
    ```
3. Change directory to the shared folder sf_NGN_Project. Under default settings run:
    ```bash
      cd /media/sf_NGN_Project
    ```
4. 


```bash
production:
python3 ngn_gui.py #  open the GUI and start controller and mininet

dev:
python3 openShellWithPy.py # open terminal and start controller and mininet
```



4. Per verificare che effettivamente vagrant è stato inserito all’interno del gruppo “vboxsf” basta scrivere:

```bash
groups vagrant
```
e vedere se tra i vari gruppi presenti c’è anche “vboxsf”


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
