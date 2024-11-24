# Project of Next Generation Networks - Automatic deployment of "containers"

> NOTE: to visualize on VSCode this file press `Ctrl+Shift+V` or `Cmd+Shift+V` on Mac

## Description

## Roadmap

1) utilizziamo le topologia già predeterminate di mininet, utilizzando il file `mn` il quale ci permette di creare una topologia di rete con più switch e più host leggendo da terminale la topologia.
 >SVANTAGGIO: tutti gli switch hanno gli stessi host, magari trovare un modo per farli variare.
2) Assegnare ad ogni host i servizi, scrivendo su un file l'IP e il nome del servizio, (servizio "data e ora" e ci collegheremo al server)
 > Assegnare dei nomi in maniera intelligente per poterli riconoscere (data è pure client e server).
3) asseganre randomicamente i servizi agli host
4) Mostrae le FlowTable e se aggregare i servizi se sono splittati (eg data e ora su server diversi)

## Requirements

- [x] Creare una repository su GitHub
- [ ] Create an SDN network in mininet with multiple switches
- [ ] Create a software that is capable of deploying services in the network
  - Services are composed of multiple applications that communicate together to deliver the service (e.g., web server and database)
- [ ] Create a GUI (python recommended) capable of:
  - Deploying service in the network (i.e., starting required applications on existing hosts)
    - Basic idea: choose host depending on usage (e.g., max 2 applications per host)
  - Choose communication requirements for applications
    - Choose communication requirements for applications
    - Choose communication requirements for applications
  - Stopping applications
    - Upon stopping, remove flows if not required anymore
- [ ] Show that applications can actually talk
  - Example of communicating applications are a web server and a database (create fake ones)

![Immage of the final project](./img/Project_SDN.png)
