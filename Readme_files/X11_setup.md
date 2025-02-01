# X11 Enable FORWARDING

`X11 forwarding is used to run graphical applications on a remote server` while displaying the user interface on a local machine.

This is commonly used in SSH (Secure Shell) connections to securely run applications with graphical user interfaces (GUIs) on a remote server and have them displayed on your local machine.

## MacOS

1. Open `XQuartz` application.

1. Open a Terminal and run:

    ```bash
        xhost + 127.0.0.1
    ```
1. Connect to the VM through SSH (on Windows machines use the MobaXterm SSH terminal):

    ```bash
        ssh -Y -p 2222 vagrant@localhost
    ```

1. Test the xclock example:

    ```bash
        xclock
    ```
    > If a clock appears, the forwarding is working

## Windows
1. Open `MobaXterm` application.
2. Open now terminal (In the top-left corner select **Terminal>Open new tab** )
 
3. Connect to the VM through SSH (on Windows machines use the MobaXterm SSH terminal):

    ```bash
        ssh -Y -p 2222 vagrant@localhost
    ```

4. Test the xclock example:

    ```bash
        xclock
    ```
    > If a clock appears, the forwarding is working

[<Back](../README.md)


