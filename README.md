# Next Generation Networks Project - Automatic deployment of "containers" - Berardo C., Castagnaro T., Consolaro J.

> NOTE: to visualize this file on VSCode press `Ctrl+Shift+V` or `Cmd+Shift+V` on Mac

- [Next Generation Networks Project - Automatic deployment of "containers" - Berardo C., Castagnaro T., Consolaro J.](#next-generation-networks-project---automatic-deployment-of-containers---berardo-c-castagnaro-t-consolaro-j)
  - [INTRODUCTION](#introduction)
    - [Presentation](#presentation)
  - [KEY FEATURES](#key-features)
  - [PREREQUISITES](#prerequisites)
  - [FILES WITH DESCRIPTION](#files-with-description)
  - [HOW TO RUN THE APPLICATION](#how-to-run-the-application)
  - [REQUIREMENTS](#requirements)

## INTRODUCTION

This project integrates Software-Defined Networking (SDN) with Mininet to dynamically deploy and manage services composed of interconnected applications. A Python-based GUI simplifies interaction and management.

### Presentation

This is the [PDF Presentation](./NGN_project.pdf) of the project.

## KEY FEATURES

- ***SDN Network***: Simulated multi-switch network in Mininet with centralized flow control via an SDN controller.
- ***Service Deployment***: Deploy and manage multi-application services with automated host selection and flow configuration.
- ***GUI***: Intuitive interface for deploying services, managing flows, and monitoring network activity.
- ***Dynamic Flow Management***: Automatically configure and clean up network flows based on application requirements.

## PREREQUISITES

- Install [Virtualbox](https://www.virtualbox.org/wiki/Downloads) and the [Comnetsemu Virtual Machine](https://drive.google.com/drive/folders/1FP5Bx2DHp7oV57Ja38_x01ABiw3wK11M?usp=sharing)
- Import `comnetsemu.ova` in Virtualbox
- Clone this repository
- Add `NGN_Project` folder as a shared folder in Comnetsemu VM settings (select automatic mounting).
- Start the VM and then connect to it via SSH with the following command (***password: vagrant***):

  ```bash
    ssh -X -p 2222 vagrant@localhost
  ```

  and run the following command to access the shared folder with privileges:

  ```bash
    sudo usermod -aG vboxsf vagrant
  ```
  Check if the `vboxsf` is in the group:

  ```bash
    groups vagrant
  ``` 
  Restart the Virtual Machine to save modifications.

- <u>***For Mac users***</u>: install [XQuartz](https://www.xquartz.org/)
- <u>***For Windows users***</u>: install [MobaXterm](https://mobaxterm.mobatek.net/download.html)
- Enable [forwarding](/Readme_files/X11_setup.md)
- Install [Python 3.7](/Readme_files/Install_Python.md) version on the VIrtual Machine. You can use terminal with SSH or directly write in the VM.

## FILES WITH DESCRIPTION
1. **ngn_gui.py**: graphical user interface
2. **topology_generator.py**: generates the topology and assign services to servers
3. **./Tools/topology_parameters.txt**: contains user-input parameters to create the topology
4. **simple_switch_stp_13.py**: contains the ryu controller configuration
5. **openShellWithPy.py**: executes shell scripts on external consoles
6. **Servers folder**: contains configuration files for servers and server's status files, that tell if they are on/off
7. **client.py**: slient configuration file
8. **img Folder**: contains images

## HOW TO RUN THE APPLICATION

1. **Open VirtualBox** and **start Comnetsemu** Virtual Machine (comnetsemu)
   
2. After boots the VM up, **for a better manageability**, instead of running commands directly into the VM it might be worth to **use your own terminal** (**or MobaXterm for Windows machine**) and ssh into the VM.
   
   To do so, run: 

   ```bash
     ssh -X -p 2222 vagrant@localhost
   ```

   > NOTE: password: vagrant

3. **Change directory** to the shared folder sf_NGN_Project. Under default settings run:
   
   ```bash
     cd /media/sf_NGN_Project
   ```

4. **Run the ngn_gui.py** program, it open the GUI and start controller and mininet:

    ```bash    
      python3.7 ngn_gui.py
    ```
5. Now you **should see some error** like: `ModuleNotFoundError: No module named 'customtkinter'` 
   
6. To **install required libraries** you must run the following scripts:

    ```bash
    python3.7 -m pip install <library_name>
    ```
    > NOTE: you probably only need to install `matplotlib` on python3.6, but it is safer to have it on both python installations, you never know :)
    
    ```bash
    python3.6 -m pip install <library_name>
    ```
    E.g.

    ```bash
    python3.7 -m pip install customtkinter
    ```
    > NOTE: you probably only need to install `matplotlib` on python3.6, but it is safer to have it on both python installations, you never know :)

    ```bash
    python3.6 -m pip install customtkinter
    ```


    Now **restart from step 4 until no error occurs**. (You should install only: `customtkinter`, `matplotlib` and `requests`)

7. Now **the program will open the Graphical User Interface and the RYU controller** will be turned-on. 
   
   *You should see the following*:

    <img src="img/gui.png" alt="Controller" width="500">
    <img src="img/controller.png" alt="Controller" width="400">

8. Use the textboxes to **set** the ***number of hosts*** and ***switches***. 
   
   Then press the button `CREATE topology` to generete the Mininet. 
   
   Wait for the topology image to display...
  
    <img src="img/Topology.png" alt="Controller" width="500">
    <img src="img/Mininet.png" alt="Controller" width="500">

9.  **Use the right-side buttons** to turn on the servers and instantiate the flows. 
    
    Once you have turned on the servers, the result appear on the GUI.
    
    <img src="img/data_service.png" alt="Controller" width="500">

10. You can also use the **mininet command line to request a service** by running the client.py program on host1 (h1) specifying the server's IP you want to connect to. 
    
    The ryu controller will automatically instantiate the required flow between the client and the server, if no flows added before.

    <img src="img/Service_request.png" alt="Controller" width="500">

11.  To delete all flows press the `REMOVE all flows button`. 
      
      This will automatically update the flow tables and delete previously added entries.

## REQUIREMENTS

- [x] Creare una repository su GitHub
- [x] Create an SDN network in mininet with multiple switches
- [x] Create a software that is capable of deploying services in the network
  - Services are composed of multiple applications that communicate together to deliver the service (e.g., web server and database)
- [X] Create a GUI (python recommended) capable of:
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
