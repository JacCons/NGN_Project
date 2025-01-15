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

- Install [Virtualbox](https://www.virtualbox.org/wiki/Downloads) and the [Comnetsemu Virtual Machine](https://drive.google.com/drive/folders/1FP5Bx2DHp7oV57Ja38_x01ABiw3wK11M?usp=sharing)
- Add NGN_Project as a shared folder in Comnetsemu VM settings.
- Connect to the VM via SSH with the following command (***password: vagrant***):

  ```bash
    ssh -X -p 2222 vagrant@localhost
  ```

  and run the following command to access the shared folder with privileges:

  ```bash
    sudo usermod -aG vboxsf vagrant
  ```
  Check if the vboxsf is in the group:

  ```bash
  groups vagrant
  ``` 

- For Mac users : install [_XQuartz_](https://www.xquartz.org/) and [enable forwarding](/Readme_files/X11_setup.md)
- For Windows users: install [_mobaXterm_](https://mobaxterm.mobatek.net/download.html) and [enable forwarding](/Readme_files/X11_setup.md)
- Install [Python 3.7](/Readme_files/Install_Python.md) version on the VIrtual Machine

## HOW TO RUN THE APPLICATION

1. Open VirtualBox and start Comnetsemu Virtual Machine (comnetsemu)
2. After logging-in, for a better “manageability”, instead of running commands directly into the VM it might be worth to use your own terminal and ssh into the VM. To do so, run:

   ```bash
     ssh -X -p 2222 vagrant@localhost
   ```

3. Change directory to the shared folder sf_NGN_Project. Under default settings run:
   
   ```bash
     cd /media/sf_NGN_Project
   ```

3.1. If some permission issues arise, then use the superuser command:

  ```bash
  sudo su
  ```

  and then repeat the previous command.

1. Run the GUI

   ```bash
   production:
   python3.7 ngn_gui.py #  open the GUI and start controller and mininet

   dev:
   python3.7 openShellWithPy.py # open terminal and start controller and mininet
   ```




## FILES WITH DESCRIPTION

## Roadmap

1. Isolate traffic between host and server
2. Fixing and improving

## Requirements

- [x] Creare una repository su GitHub
- [x] Create an SDN network in mininet with multiple switches
- [x] Create a software that is capable of deploying services in the network
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
