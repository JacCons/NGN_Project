### X11 FORWARDING

**MacOS**

0. Open XQuartz Application.

1. Open a Terminal and run:

    ```bash
        xhost + 127.0.0.1
    ```

**Windows**
1. Creare una nuova sessione SSH inserendo remote host: 127.0.0.1 e verificando che l’X11 forwarding sia attivo nella sezione “Advanced SSH settings” **************not clear
 
### TEST IF X11 or mobaXterm WORK

1. Connect to the VM through SSH:

    ```bash
        ssh -Y -p 2222 vagrant@localhost
    ```

2. Test the xclock example:

    ```bash
        xclock
    ```
If a clock appears, the forwarding is working

[<Back](README.md)

<!-- 6. Per verificare che effettivamente vagrant è stato inserito all’interno del gruppo “vboxsf” basta scrivere:
	
```bash
groups vagrant
```
e vedere se tra i vari gruppi presenti c’è anche “vboxsf” -->

