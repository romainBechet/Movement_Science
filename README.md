# In Progress

## Table of Content

1. [Damped Filter](#damped_filter)
2. [Static](#static)

Few programs to analyze data collected on humans.

The aim is to write again the scripts I used in the past, and make them more usable and flexible for different purposes. For each one, a example is done with real data to show how to use each class (`{name}_demo.ipynb`). Some open-source data coming from published articles can be used. In this case, authors and the article will be mentioned. 

The folder is in progress, some classes are not finished yet and can be improved. 

## Damped Filter: <a name="damped_filter"></a>
Critically Damped Filter for sudden movements. The filter can be used for Ground Reaction Forces (GRF) during locomotion or jumpping, as well as for kinematics data depending on the movement type. 

Formula validation by Robertson DG, Dowling JJ. Design and responses of Butterworth and critically damped digital filters. J Electromyogr Kinesiol. 2003 Dec;13(6):569-73. doi: 10.1016/s1050-6411(03)00080-4. PMID: 14573371 ([full PDF](https://www.researchgate.net/publication/9043065_Design_and_responses_of_Butterworth_and_critically_damped_digital_filters)). 

The class is programmed to make low pass only.

__Ouputs:__
- Filtered signals 

__Plotting:__ 
- Raw and filtered data (Possible to plot Butterworth filtered signals to compare)

![alt-text](https://github.com/romainBechet/Movement_Science/blob/master/images/readme/running.png)

#### Data: 
- Personal data from a Bertec Instrumented treadmill. 

#### How to use?
- Import the module: 
```python 
from damped_filter import Signal 
``` 
- Create an instance of the class: Arguments = data and frequency 
```python
walking = Signal(data, 2000)
```

- Filtering the signals with the Critically Damped: Arguments = Order and cutoff frequency
```python
walking.critically_damped(4, 25)
```

- Plot signals: Default Arguments = plot_classic_butterworth = True, save_plot and plot_name = False. 
```python 
walking.plot_raw_and_filtered(plot_classic_butterworth = True, save_plot = True, plot_name = '')
```


## Static: <a name="static"></a>
Data analysis for Postural static measurement with basic force plate. 



__Calculated parameters:__
- Mean Position
- Length of the Center of Pressure (COP)
- Length of the COP
- Range
- Standard Deviation
- Velocity 
- Ellipse Area

Parameters from [Paillard T, Noé F. Techniques and Methods for Testing the Postural Function in Healthy and Pathological Subjects. Biomed Res Int. 2015;2015:891390. doi:10.1155/2015/891390](https://pubmed.ncbi.nlm.nih.gov/26640800/) (Chapter 5.1.2)

__Plotting:__
- Center of Pressure path 
- Ellipse Area 

![alt -text](https://github.com/romainBechet/Movement_Science/blob/master/images/readme/static.png)

''' TODO ''' 
- Frequency Analysis 

#### Data: 
- Personal data from a Kistler Force Plate 

#### How to use?
- Import the module: 
```python 
from static import Static
``` 
- Create an instance of the class: Arguments = Positions x and y, frequency
```python
name_of_instance = Static(x, y, fs)
```

- Draw the ellipse with desired confience interval: 
```python
name_of_instance.draw_ellipse_confidence(conf = 0 < conf < 1.0 (optional, default = 0.95), **kwargs)
```

- Get all parameters:
```python 
name_of_instance.get_parameters(conf = 0 < conf < 1.0 (optional, default = 0.95))
```
