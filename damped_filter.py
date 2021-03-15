
import math 
from scipy import signal
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Signal(): 

    def __init__(self, signals: [], fs: int): 
        self.signals = signals 
        self.fs = fs
        self.time = np.linspace(0, len(self.signals)/self.fs, len(self.signals))

    def critically_damped(self, filter_passes: int, fc: float) -> pd.DataFrame: 
        """Filters the signals with the Critically Damped filter. 

        Args:
            filter_passes (int): Number of passes
            fc (float): Cutoff frequency

        Returns:
            pd.DataFrame: Filtered signals
        """
        
        b, a = self.critically_damped_coefficients(filter_passes, fc)
        self.filtered_signals = []

        signals_name = self.signals.columns
        for sig in signals_name: 
            self.filtered_signals.append(signal.filtfilt(b, a, self.signals[sig]))
        
        self.damped_signals = pd.DataFrame({signals_name[i]: self.filtered_signals[i] for i in range(len(signals_name))})

        return self.damped_signals

    def plot_raw_and_filtered(self, plot_classic_butterworth: bool = True, save_plot:bool = False, plot_name: str= 'filter_signals',
                            color_raw = 'grey', label_raw = 'Raw Data', style_raw = '-', width_raw = 1,
                            color_damped = 'b', label_damped = 'Critically Damped', style_damped = '-', width_damped = 1,
                            color_butter = 'r', label_butter = 'Classic Butterworth', style_butter = '-', width_butter = 1): 

        """Plot Raw and filtered data 
        If signals are not filtered yet, the filter passes and cutoff frequency are requested. 

        Args: 
            plot_classic_butterworth (bool): Plot or not to compare (Default: True)
            save_plot (bool): Explicit no? (Default: False)
            plot_name (str): Explicit too? (Default: 'filter_signals')

            
            color, label, style, and width (completed by _raw or _damped or _butter

        """

        try: 
            self.damped_signals
        except AttributeError: 
            self.filter_passes = int(input("You don't have filtered your signal(s) yet. Please type the order of the filter (a number): "))
            self.fc = float(input("Now, type the cutoff frequency for the filter (a number): "))

            self.critically_damped(self.filter_passes, self.fc)


        n_plot = len(self.signals.columns)
        signals_name = self.signals.columns
        fig, axs = plt.subplots(n_plot, 1, sharex = True, figsize = (20,10))
        for p in range(n_plot): 
            axs[p].plot(self.time, self.signals[signals_name[p]], color = color_raw, label = label_raw, ls = style_raw, lw = width_raw)
            axs[p].plot(self.time, self.damped_signals[signals_name[p]], color = color_damped, label = label_damped, ls = style_damped, lw = width_damped)
            axs[p].legend()
            axs[p].set_ylabel(signals_name[p])
        
        axs[-1].set_xlabel('Time (s)')
        axs[-1].set_xlim(0, self.time.max())

        if plot_classic_butterworth == True: 
            self.classic_butterworth()
            for p in range(n_plot): 
                axs[p].plot(self.time, self.butter_signals[signals_name[p]], color = color_butter, label = label_butter, ls = style_butter, lw = width_butter)
                axs[p].legend()


        if save_plot == True: 
            name = f'{plot_name}.png'
            plt.savefig(name, transparent=False, dpi = 180, bbox_inches="tight")
         

    def critically_damped_coefficients(self, filter_passes, fc):
        """Compute the coefficients A & B
        """
        self.filter_passes = filter_passes
        self.fc = fc
        # Correction of the Cutoff Frequency
        c_critical = 1 / (((2**(1/(2*self.filter_passes)))-1)**(1/2))
        f_adjusted_critical = self.fc * c_critical

        w_adjusted_critical = math.tan(math.pi * f_adjusted_critical / self.fs)

        k1_critical = 2 * w_adjusted_critical
        k2_critical = w_adjusted_critical **2


        # A & B coefficients
        b0_critical = b2_critical =  k2_critical / (1 + k1_critical + k2_critical)
        b1_critical = 2 * b0_critical

        a1_critical = 2 * b0_critical * (1/k2_critical -1)
        a2_critival = 1 - (b0_critical + b1_critical + b2_critical + a1_critical)

        b = [b0_critical, b1_critical, b2_critical]
        a = [1, - a1_critical, - a2_critival]

        return b, a

    def classic_butterworth(self): 
        """ Classic Butterworth filtering
        """
        Wn = self.fc / (self.fs /2)
        b, a = signal.butter(self.filter_passes, Wn)

        butter_signals = []
        signals_name = self.signals.columns
        for sig in signals_name: 
            butter_signals.append(signal.filtfilt(b, a, self.signals[sig]))
        
        self.butter_signals = pd.DataFrame({signals_name[i]: butter_signals[i] for i in range(len(signals_name))})