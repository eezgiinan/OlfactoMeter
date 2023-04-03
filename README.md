# Olfactometer!

<p align="center">
<img src="https://user-images.githubusercontent.com/126763830/229083268-6e085a2a-17c1-4e72-8011-350dfe3abf9c.PNG" width="650" height="400">
</p>

## Contributors
- Aurore de la Fouchardière
- Adrien d'Hollande
- Elif Ezgi Inan

<!-- ABOUT THE PROJECT -->
## About The Project

Here we present the user interface (UI) for a custom-made olfactometer created for BioFabLab projects in BME Paris program. The interface is intended to be used connected to the device. Olfactometer is an instrument used for delivering odors to a subject in a controlled manner. It has been used for behavioral experiments to assess the effect of olfactory stimulus in the brain. 

This UI allows the user to control the delivery of two different odors using four different modes: *Resting*, *Purging*, *Odor 1*, and *Odor 2*. Delivery of these odors is mutually exclusive, meaning that only one odor can be delivered at a time. Therefore, purging between experiments is necessary to make sure that there is no odor from the previous experiment. The modes are controlled by four solenoid valves, namely; S<sub>A</sub>, S<sub>B</sub>, S<sub>1</sub> and S<sub>2</sub>. S<sub>A</sub> valve controls the entry of air into the system which means it is always open when an experiment is started. S<sub>B</sub> valve opens when purging is activated. Finally, S<sub>1</sub> and S<sub>2</sub> valves are open when first and second odor is delivered, accordingly. 

For more information on the project, please visit our webpage: [tiki_wiki](https://wiki.bme-paris.com/2023-project09/tiki-index.php?page=HomePage).

Olfactometer used with the interface  |  The olfactometer itself
:-------------------------:|:-------------------------:
![](https://user-images.githubusercontent.com/126763830/229479623-745d6f13-aac3-4710-8488-a271be16636d.PNG)  |  ![](https://user-images.githubusercontent.com/126763830/229479766-1c75f2cc-9ce4-4f01-89a6-569a76d4c062.jpeg)

<!-- GETTING STARTED -->
## Getting Started
This interface contains manual and automatic control for the selection of a mode and a duration, along with a feedback section for analysis of the ongoing experiments. In the feedback section, there are circles that represent the valves and show the currently activated mode, accompanying a plot representing the progress of the experiment. There is also a button for an emergency stop which activates *Purging* for 10 seconds to clean the tube and then stops. Additionally, information regarding odor names, protocol name and mouse ID could be saved in the computer. When an experiment is started using either Manual or Excel Control, the program automatically saves the experiment in the code editor under a protocol name. This happens when the program is closed.

### Need to know
There are some steps to be followed by the user to start using the program successfully. 
- PORT in *app.py* should be changed according to the computer. It is set to COM3 as default.
- Certain libraries need to be installed (ex. Matplotlib) in the computer. This can be done easily on PyCharm.
- If the user wishes to use the Manual Control option when launching the interface, they should click on the *Reset History* button before clicking on *Run*. Failure to do so may result in an error message. However, once the interface is running, clicking on the button is not necessary.

### Good to know
The application is constructed using model-view-controller (MVC) system. This design pattern is used when an application gets more complex over time so different sections are seperated to make it more manageable. It was decided to implement this system to improve further modification in the future. More information on how MVC works and its implementation can be found here: https://www.pythontutorial.net/tkinter/tkinter-mvc/ 


<!-- ACKNOWLEDGMENTS -->

## Acknowledgements

This project is created by BME Paris students in Universite Paris Cité as a part of the Master's program, in collaboration with Vetere Lab at ESPCI in Paris, France.
We would like to thank Gisella Vetere, Clement Pouget and Maelle Christaens for their help and insights during the entire project.
