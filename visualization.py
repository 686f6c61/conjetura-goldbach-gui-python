"""
Visualization functions for the Goldbach Conjecture.

This module provides specialized visualization tools for representing Goldbach Conjecture data.
It includes functions for creating scatter plots of prime pairs and histograms of pair counts,
as well as utilities for embedding these visualizations in a tkinter GUI.

Author: https://github.com/686f6c6
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_scatter_plot(pairs_dict, figure=None):
    """
    Create a scatter plot showing prime pairs for each even number.
    
    This function generates a scatter plot where each point represents a pair of primes
    that sum to a particular even number. Different colors are used to distinguish pairs
    for different even numbers. A diagonal line is added to show the symmetry of the pairs.
    
    Args:
        pairs_dict (dict): Dictionary with even numbers as keys and list of prime pairs as values
                          Format: {even_number: [(p1, p2), ...], ...}
        figure (matplotlib.figure.Figure, optional): Figure to plot on. If None, a new figure is created.
        
    Returns:
        matplotlib.figure.Figure: The figure containing the plot
    
    Note:
        For best visual clarity, this function works best with a limited number of even numbers.
        When plotting many even numbers, the legend is automatically hidden to prevent clutter.
    """
    if figure is None:
        figure = plt.figure(figsize=(10, 6))
    
    ax = figure.add_subplot(111)
    
    # Process data for plotting
    for even_num, pairs in pairs_dict.items():
        x_values = [pair[0] for pair in pairs]
        y_values = [pair[1] for pair in pairs]
        ax.scatter(x_values, y_values, label=f"{even_num}", alpha=0.7)
    
    ax.set_xlabel('Primer primo')
    ax.set_ylabel('Segundo primo')
    ax.set_title('Conjetura de Goldbach: pares de primos para números pares')
    
    # Add diagonal line y = x to show symmetry
    max_val = max([max(pair) for pairs in pairs_dict.values() for pair in pairs]) if pairs_dict else 0
    ax.plot([0, max_val], [0, max_val], 'k--', alpha=0.3)
    
    # Add a legend if there aren't too many numbers
    if len(pairs_dict) <= 10:
        ax.legend(title="Número par")
    
    ax.grid(True, alpha=0.3)
    
    return figure

def create_histogram(counts_dict, figure=None):
    """
    Create a histogram showing the number of prime pairs for each even number.
    
    This function generates a bar chart where each bar represents an even number,
    and the height of the bar indicates how many distinct prime pairs sum to that number.
    The exact count is displayed on top of each bar for precise reference.
    
    Args:
        counts_dict (dict): Dictionary with even numbers as keys and count of prime pairs as values
                           Format: {even_number: count, ...}
        figure (matplotlib.figure.Figure, optional): Figure to plot on. If None, a new figure is created.
        
    Returns:
        matplotlib.figure.Figure: The figure containing the plot
    
    Note:
        This visualization is particularly useful for observing patterns in the number of
        Goldbach pairs as even numbers increase, which relates to the density of primes.
    """
    if figure is None:
        figure = plt.figure(figsize=(10, 6))
    
    ax = figure.add_subplot(111)
    
    even_numbers = list(counts_dict.keys())
    counts = list(counts_dict.values())
    
    bars = ax.bar(even_numbers, counts, alpha=0.7)
    
    # Add count labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
    
    ax.set_xlabel('Número par')
    ax.set_ylabel('Cantidad de pares primos')
    ax.set_title('Conjetura de Goldbach: cantidad de pares primos por número par')
    ax.grid(True, alpha=0.3, axis='y')
    
    return figure

def embed_plot_in_tkinter(figure, frame):
    """
    Embed a matplotlib figure in a tkinter frame.
    
    This utility function bridges matplotlib and tkinter by creating a canvas
    that can display a matplotlib figure within a tkinter GUI. The figure is
    automatically sized to fill the available space in the frame.
    
    Args:
        figure (matplotlib.figure.Figure): The matplotlib figure to embed
        frame (tkinter.Frame): The tkinter frame to embed the figure in
        
    Returns:
        FigureCanvasTkAgg: The canvas containing the embedded figure, which can
                          be used for further customization or to add a toolbar
    
    Note:
        The caller is responsible for packing or otherwise managing the layout
        of the frame that contains the embedded figure.
    """
    canvas = FigureCanvasTkAgg(figure, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    return canvas
