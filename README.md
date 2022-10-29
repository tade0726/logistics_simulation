# A simulation of a conveying-transport system for parcel redistribution


A simple demo how to simulation a conveying-transport for logistics business, for example (https://www.ssi-schaefer.com/en-au/products/conveying-transport)


![conveying](container-and-carton-conveyor-system-dam-image-en-1029-.png)


## The codes structure

data: demo data
demo: a demo from simpy C-plan
docs: dev docs, process diagram, explantion of each CLASS
logs: logs
src: 
- controllers: a control and monitoring module for the simulation
- db: function related to database operation
─ machine: python CLASS wrriten to reflex the logic of a facotry machine
- utils: helper function
- vehicles: python CLASS describing vehicles 
