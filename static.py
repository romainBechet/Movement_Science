import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2
import matplotlib.pyplot as plt
import math

class Static(): 

    def __init__(self, ML, AP, fs):
        self.x = np.array(ML)
        self.y = np.array(AP)
        self.fs = fs 
        self.period = 1/ self.fs
        self.ellipse_parameters = dict()
        self.parameters = dict()
        

    def get_parameters(self, conf: float = 0.95): 
        """ Return all parameters we can get with a static analysis. 
        Parameters are calculated if they're not existing yet.
        For more information on parameters: Paillard T, Noé F. Techniques and Methods for Testing the Postural Function in Healthy and Pathological Subjects. Biomed Res Int. 2015;2015:891390. doi:10.1155/2015/891390

        Args: 
            [conf]: float for confidence interval for the ellipse, default 0.95

        Returns:
            [dict]: parameters
        """
        try: 
            int(self.ellipse_parameters['area'])
        except: 
            self.confidence_ellipse_interval(conf = conf)

        self.calculate_params()
        self.parameters['area_cop'] = self.ellipse_parameters['area']
        
        return self.parameters

    def calculate_params(self, conf: float = 0.95): 
        """
        Calculate the major part of parameters we can get with a static analysis. 

        Output: 
            Update self.parameters with the parameters 
            For parameters depending on the axis (x,y -- or medio-lateral, antero-posterior),
            They are presented into arrays [x, y]

            All parameters are accessible typing instance.get_parameters()

        """
        
        # Mean Position
        self.parameters['mean_position'] = [self.x.mean(), self.y.mean()]
        
        # Displacement and length of the COP
        displacement_x = [ np.abs(self.x[i+1] - self.x[i]) for i in range(len(self.x) -1) ]
        displacement_y = [np.abs(self.y[i+1] - self.y[i]) for i in range(len(self.y) -1)]
        displacement_total = [np.sqrt(displacement_x[i]**2 + displacement_y[i]**2) for i in range(len(displacement_x))]
        self.parameters['lenght_cop'] = np.sum(displacement_total)

        # Range of movement
        self.parameters['range'] = [self.x.max() - self.x.min(), self.y.max() - self.y.min()]
        
        # Standard Deviation of the movement
        self.parameters['standard_deviation'] = [self.x.std(), self.y.std()]
        
        # Speed of the movement 
        movement_speed_x = [displacement_x[i] / self.period for i in range(len(displacement_x))]
        movement_speed_y = [displacement_y[i] / self.period for i in range(len(displacement_y))]
        movement_speed = [displacement_total[i] / self.period for i in range(len(displacement_total))]

        self.parameters['speed_by_axis'] = [np.mean(movement_speed_x), np.mean(movement_speed_y)]
        self.parameters['speed_total'] = np.mean(movement_speed)

        # Freq analysis
        ''' TODO Frequency analysis''' 
  

    def confidence_ellipse_interval(self, conf: float = 0.95): 
        """
        Calculate parameters for plotting and characterizing ellipse around the cop path. 

        Args:
            conf (float, optional): Confidence interval desired. Defaults to 0.95.

        Returns: 
            Updating parameters `self.ellipse_parameters`
            Return (x,y) coordinates for plotting the ellipse, with `draw_ellipse_confidence_interval()` method. 
        """

        def cart2pol(x, y):
            rho = np.sqrt(x ** 2 + y ** 2)
            phi = np.arctan2(y, x)
            return (rho, phi)

        def ell_points(C): 
            n = 100 
            p = [i * (math.pi / n) for  i in range(201)]
            eigval, eigvec = np.linalg.eigh(C)
            z = eigval[0]
            v = eigval[1]
            eigval = np.array([[z,0], [0, v]])
            a = [math.cos(p[i]) for i in range(len(p))]
            b = [math.sin(p[i]) for i in range(len(p))]
            c = np.array([a,b]).transpose()
            xy = np.dot(c, np.sqrt(eigval))
            xy = np.dot(xy, eigvec.transpose())
            x = xy[:,0]
            y = xy[:,1]
            return x,y    


        def draw_elli(C, conf, Pangles, meandata):

            dof, c = np.shape(C)
            rv = chi2.ppf(conf,c)
            k = np.sqrt(rv)
            x, y = ell_points(C)

            path_ellipse = [(k*x) + meandata[0], (k*y) + meandata[1]]


            rads, angs = cart2pol((k*x), (k*y))
            Pradi = np.argmin(abs(angs - Pangles[0]))
            Sradi = np.argmin(abs(angs - Pangles[1]))
            bothRad = [rads[Pradi], rads[Sradi]]


            return path_ellipse, bothRad  

        

        x = self.x
        y = self.y 
        self.ellipse_parameters['interval_confidence'] = conf

        meandata = [x.mean(), y.mean()]

        if x.size != y.size:
            raise ValueError("x and y must be the same size")

        cov = np.cov(x, y)

        ev, a = np.linalg.eig(cov)
        
        ev = np.sort(ev)
        ind = ev.argsort()

        self.ellipse_parameters['eigval'] = [np.sqrt(ev[1]), np.sqrt(ev[0])]

        # Extract the angle of the major axis: 
        xa, ya = a[0, ind[1]], a[1, ind[1]]

        angleP = np.arctan2(ya, xa)
        ellipse_anglePdeg = angleP * 180 / math.pi
        # Limit range to [0 - 180]
        if ellipse_anglePdeg < 0: 
            ellipse_anglePdeg += 180 
            angleP += math.pi

        # Extract the angle of the secondary axis
        xa2, ya2 = a[0,0], a[1, 0]

        angleS = np.arctan2(ya2, xa2)
        ellipse_angleSdeg = angleS *180 / math.pi 
        # Limit range to [0,180]
        if ellipse_angleSdeg < 0: 
            ellipse_angleSdeg += 180 
            angleS += math.pi
        
        bothangs = [angleP, angleS]

        self.ellipse_parameters['axis_angle'] = bothangs
        self.ellipse_parameters['path_ellipse'], axislenght  = draw_elli(cov, conf, bothangs, meandata)
        self.ellipse_parameters['area'] = math.pi * axislenght[0] * axislenght[1]
        self.ellipse_parameters['axis_length'] = axislenght
        self.ellipse_parameters['ratio'] = axislenght[0] / axislenght[1]

        return self.ellipse_parameters['path_ellipse']


    def draw_ellipse_confidence_interval(self, conf: float = 0.95, path_style: str = '-', path_color:str = 'black', **kwargs):
        """
        Draw the cop and the ellipse with the chosen confidence interval. 

        Args:
            conf (float, optional): Confidence interval desired. Defaults to 0.95.
            path_style (str, optional): Style for the cop path. Defaults to '-', available: '-', '--', '-.', ':'
            path_color (str, optional): Color for the cop path. Defaults to 'black', available: all colors used in matplotlib. 

            **kwargs (optional): Style for the ellipse
                Forwarded to `~matplotlib.lines.Lines2D`, more information here: `https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html`

        """


        if path_style not in ['-', '--', '-.', ':']: 
            raise Exception("'{0}' not known as path_style.\npath_style should be either '-' (solid line), '--' (dashed line), '-.' (dash-dotted line) or ':' (dotted line).\nFor more information: https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D.set_linestyle ".format(path_style))

        fig, ax = plt.subplots()
        ax.plot(self.x, self.y, ls = path_style, color = path_color)
        p = self.confidence_ellipse_interval(conf)
        ax.plot(p[0], p[1], **kwargs)

        
        ax.axis('equal')
        plt.show()
                 
            
    

        
    