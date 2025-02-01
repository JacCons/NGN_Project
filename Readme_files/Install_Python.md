# Why python3.7 instead of python3.6.9?

The objective is to run the ***GUI with python 3.7*** - because `customtkinter` libraries does not support python3.6 -, while all ***other scripts*** have to be run ***with python3.6***.


## Installing python 3.7

1. To install Python3.7 run:

    ```bash	
        sudo apt update
        sudo apt install -y python3.7
    ```

2. Upgrade pip:

    ```bash	
        python3.7 -m pip install --upgrade pip
    ```

3. Ensure Python3.7 and pip are correctly installed:
	
    ```bash
        python3.7 --version
    ```
    Output should be something like: `Python 3.7.X `

    ```bash
        python3.7 -m pip --version
    ```
    Output should be something like: `pip X.X.X from path/lib/python3.7/site-packages (python 3.7)`

4. Execute these commands to choose the Python version:
	
    ```bash  
        sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
    ```
    ```bash
        sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 2 
    ```
    ```bash
        sudo update-alternatives --config python3
    ```
    `Select 1` and choose Python 3.6.9 as Python3 default version (***necessary to run mininet***)

## Libraries used

To see witch libraries we used, take a look at the [requirements.txt](./requirements.txt) file.


[<Back](../README.md)