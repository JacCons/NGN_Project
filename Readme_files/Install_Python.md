## Why python3.7 instead of python3.6.9?
The objective is to run the GUI with python 3.7, while all other scripts have to be run with python3.6 (because of compatibility issues)

# INSTALLING PYTHON 3.7

1. To install Python3.7 run:

    ```bash	
        sudo apt update
        sudo apt install -y python3.7
    ```

2. Upgrade/Install pip: #************************** not clear

    ```bash	
        python3.7 -m ensurepip —upgrade (di solito non funziona)
        python3.7 .m pip install —upgrade pip
    ```

3. Ensure Python3.7 and pip are correctly installed:
	
    ```bash
        python3.7 —version
    ```

    ```bash
        python3.7 -m pip —version
    ```
Output should be something like: pip X.X.X from /usr/lib/python3.7/site-packages (python 3.7)

4. Execute these commands to choose the Python version:
	
    ```bash  
        sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1 
        sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 2 
        sudo update-alternatives --config python3
    ```
Select “1” and choose Python 3.6.9 as Python3 default version (necessary to run mininet)

5. To install required libraries to run the program, see the [requirements](requirements.txt) file:
	
    ```bash
        python3.7 -m pip install <library_name>
    ```

[<Back](README.md)