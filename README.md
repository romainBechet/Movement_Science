# In Progress

Few programs to analyze data collected on humans.

The aim is to write again the scripts I used in the past, and make them more usable and flexible for different purposes.For each one, a example is done with real data to show how to use each class (`{name}_demo.ipynb`). Some open-source data coming from opublished articles can be used. In this case, authors and the article will be mentioned. 

The folder is in progress, some classes are not finished yet and can be improved. 

## Static: 
Data analysis for Postural static measurement with basic force plate. 

**Calculated parameters: **
- Mean Position
- Length of the Center of Pressure (COP)
- Length of the COP
- Range
- Standard Deviation
- Velocity 
- Ellipse Area

Parameters from [Paillard T, Noé F. Techniques and Methods for Testing the Postural Function in Healthy and Pathological Subjects. Biomed Res Int. 2015;2015:891390. doi:10.1155/2015/891390](https://pubmed.ncbi.nlm.nih.gov/26640800/) (Chapter 5.1.2)

**Plotting: **
- Center of Pressure path 
- Ellipse Area 

![alt -text](images\readme\static.png)

''' TODO ''' 
- Frequency Analysis 

#### Data: 
- Personal data from Kistler Force Plate 

#### How to use?
- Import the module: 
```python 
from static import Static
``` 
- Create an instance of the class: 
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
