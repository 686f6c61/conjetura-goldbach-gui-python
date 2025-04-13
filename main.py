"""
Main entry point for the Goldbach Conjecture visualization application.

This module implements the graphical user interface for visualizing the Goldbach Conjecture.
It provides an interactive environment for analyzing how even numbers can be expressed
as the sum of two prime numbers, with various visualization options.

Author: https://github.com/686f6c6
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

from prime_utils import is_prime, generate_primes
from goldbach import find_goldbach_pairs, count_goldbach_pairs, analyze_goldbach_range
from visualization import create_scatter_plot, create_histogram, embed_plot_in_tkinter

class GoldbachApp:
    """
    Main application class for the Goldbach Conjecture visualization.
    
    This class manages the entire application flow, including:
    - Creating and managing the user interface
    - Handling user interactions
    - Processing data for visualization
    - Displaying results in various formats
    """
    def __init__(self, root):
        """
        Initialize the application with the given root window.
        
        Args:
            root (tk.Tk): The root window for the application
        """
        self.root = root
        self.root.title("Conjetura de Goldbach - Visualización")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12))
        self.style.configure("TLabel", font=("Arial", 12))
        self.style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        
        # Create main container
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Show welcome screen initially
        self.show_welcome_screen()
    
    def open_github_link(self):
        """
        Open the GitHub repository link in the default web browser.
        """
        import webbrowser
        webbrowser.open_new("https://github.com/686f6c6")
    
    def show_welcome_screen(self):
        """
        Display the welcome screen with application information and navigation options.
        """
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Welcome title
        welcome_frame = ttk.Frame(self.main_frame)
        welcome_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        title_label = ttk.Label(
            welcome_frame, 
            text="Bienvenido a la visualización de la conjetura de Goldbach",
            style="Title.TLabel"
        )
        title_label.pack(pady=20)
        
        # Description
        description_text = """
La conjetura de Goldbach establece que todo número par mayor que 2 
puede expresarse como la suma de dos números primos.

Esta aplicación te permite:
• Encontrar pares de números primos que suman a un número par
• Visualizar estos pares en un gráfico de dispersión
• Ver un histograma de cuántas combinaciones hay para cada número par
        """
        
        description = scrolledtext.ScrolledText(
            welcome_frame, 
            wrap=tk.WORD, 
            width=60, 
            height=10,
            font=("Arial", 12)
        )
        description.insert(tk.INSERT, description_text)
        description.configure(state='disabled')
        description.pack(pady=10, padx=20)
        
        # Menu buttons
        button_frame = ttk.Frame(welcome_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(
            button_frame, 
            text="Analizar un número par",
            command=self.show_single_number_screen,
            width=25
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        ttk.Button(
            button_frame, 
            text="Analizar un rango de números",
            command=self.show_range_analysis_screen,
            width=25
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        # Credits and GitHub link frame
        credits_frame = ttk.Frame(welcome_frame)
        credits_frame.pack(side=tk.BOTTOM, pady=10, fill=tk.X)
        
        # Credits label
        credits_label = ttk.Label(
            credits_frame, 
            text="Desarrollado para visualizar la conjetura de Goldbach - 2025",
            font=("Arial", 10)
        )
        credits_label.pack(side=tk.LEFT, padx=10)
        
        # GitHub link
        github_link = ttk.Label(
            credits_frame,
            text="GitHub: https://github.com/686f6c6",
            font=("Arial", 10),
            foreground="blue",
            cursor="hand2"
        )
        github_link.pack(side=tk.RIGHT, padx=10)
        
        # Bind click event to open GitHub in browser
        github_link.bind("<Button-1>", lambda e: self.open_github_link())
    
    def show_single_number_screen(self):
        """
        Display the screen for analyzing a single even number.
        
        This screen allows the user to input an even number and view all prime pairs
        that sum to that number, along with a visualization.
        """
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Back button
        back_button = ttk.Button(
            self.main_frame, 
            text="← Volver al Menú",
            command=self.show_welcome_screen
        )
        back_button.pack(anchor=tk.NW, pady=10)
        
        # Title
        title_label = ttk.Label(
            self.main_frame, 
            text="Analizar un número par",
            style="Title.TLabel"
        )
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = ttk.Frame(self.main_frame)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Ingrese un número par mayor que 2:").pack(side=tk.LEFT, padx=5)
        
        self.number_entry = ttk.Entry(input_frame, width=10, font=("Arial", 12))
        self.number_entry.pack(side=tk.LEFT, padx=5)
        self.number_entry.insert(0, "10")  # Default value
        
        analyze_button = ttk.Button(
            input_frame, 
            text="Analizar",
            command=self.analyze_single_number
        )
        analyze_button.pack(side=tk.LEFT, padx=5)
        
        # Results frame
        self.results_frame = ttk.Frame(self.main_frame)
        self.results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def analyze_single_number(self):
        """
        Process and display results for a single even number analysis.
        
        This method:
        1. Validates user input
        2. Finds all prime pairs that sum to the given even number
        3. Displays the results in text format
        4. Creates and displays a scatter plot visualization
        """
        try:
            number = int(self.number_entry.get())
            
            if number <= 2:
                messagebox.showerror("Error", "El número debe ser mayor que 2")
                return
            
            if number % 2 != 0:
                messagebox.showerror("Error", "El número debe ser par")
                return
            
            # Clear previous results
            for widget in self.results_frame.winfo_children():
                widget.destroy()
            
            # Find Goldbach pairs
            pairs = find_goldbach_pairs(number)
            
            if not pairs:
                messagebox.showerror("Error", f"No se encontraron pares para {number}")
                return
            
            # Display results
            result_text = f"Se encontraron {len(pairs)} pares de números primos que suman {number}:\n\n"
            for p1, p2 in pairs:
                result_text += f"{p1} + {p2} = {number}\n"
            
            # Text results
            text_frame = ttk.LabelFrame(self.results_frame, text="Resultados")
            text_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=5, pady=5)
            
            result_text_widget = scrolledtext.ScrolledText(
                text_frame, 
                wrap=tk.WORD,
                width=30,
                height=15
            )
            result_text_widget.insert(tk.INSERT, result_text)
            result_text_widget.configure(state='disabled')
            result_text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Visualization
            viz_frame = ttk.LabelFrame(self.results_frame, text="Visualización")
            viz_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT, padx=5, pady=5)
            
            # Create figure for the plot
            fig = plt.figure(figsize=(6, 5))
            
            # Scatter plot of prime pairs
            ax = fig.add_subplot(111)
            x_values = [pair[0] for pair in pairs]
            y_values = [pair[1] for pair in pairs]
            ax.scatter(x_values, y_values, color='blue', alpha=0.7)
            
            # Add labels for each point
            for i, (x, y) in enumerate(zip(x_values, y_values)):
                ax.annotate(f"({x},{y})", (x, y), textcoords="offset points", 
                           xytext=(0, 5), ha='center')
            
            ax.set_xlabel('Primer Primo')
            ax.set_ylabel('Segundo Primo')
            ax.set_title(f'Pares de primos que suman {number}')
            ax.grid(True, alpha=0.3)
            
            # Embed plot in tkinter
            canvas = FigureCanvasTkAgg(fig, master=viz_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Add toolbar
            toolbar = NavigationToolbar2Tk(canvas, viz_frame)
            toolbar.update()
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un número válido")
    
    def show_range_analysis_screen(self):
        """
        Display the screen for analyzing a range of even numbers.
        
        This screen allows the user to input a range of even numbers and view
        visualizations of the Goldbach pairs across that range.
        """
        # Clear main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Back button
        back_button = ttk.Button(
            self.main_frame, 
            text="← Volver al Menú",
            command=self.show_welcome_screen
        )
        back_button.pack(anchor=tk.NW, pady=10)
        
        # Title
        title_label = ttk.Label(
            self.main_frame, 
            text="Analizar un rango de números pares",
            style="Title.TLabel"
        )
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = ttk.Frame(self.main_frame)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Desde:").pack(side=tk.LEFT, padx=5)
        self.start_entry = ttk.Entry(input_frame, width=8, font=("Arial", 12))
        self.start_entry.pack(side=tk.LEFT, padx=5)
        self.start_entry.insert(0, "4")  # Default value
        
        ttk.Label(input_frame, text="Hasta:").pack(side=tk.LEFT, padx=5)
        self.end_entry = ttk.Entry(input_frame, width=8, font=("Arial", 12))
        self.end_entry.pack(side=tk.LEFT, padx=5)
        self.end_entry.insert(0, "20")  # Default value
        
        analyze_button = ttk.Button(
            input_frame, 
            text="Analizar",
            command=self.analyze_range
        )
        analyze_button.pack(side=tk.LEFT, padx=5)
        
        # Results frame
        self.range_results_frame = ttk.Frame(self.main_frame)
        self.range_results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def analyze_range(self):
        """
        Process and display results for a range of even numbers.
        
        This method:
        1. Validates user input for the range
        2. Analyzes all even numbers in the specified range
        3. Creates and displays multiple visualizations:
           - Scatter plot of prime pairs
           - Histogram of pair counts
           - Data table with detailed information
        """
        try:
            start = int(self.start_entry.get())
            end = int(self.end_entry.get())
            
            if start < 4:
                start = 4  # Ensure start is at least 4
            
            if end < start:
                messagebox.showerror("Error", "El valor final debe ser mayor que el inicial")
                return
            
            if end > 100:
                response = messagebox.askquestion(
                    "Advertencia", 
                    "Analizar un rango grande puede llevar tiempo. ¿Desea continuar?"
                )
                if response != 'yes':
                    return
            
            # Clear previous results
            for widget in self.range_results_frame.winfo_children():
                widget.destroy()
            
            # Analyze range
            pairs_dict, counts_dict = analyze_goldbach_range(start, end)
            
            if not pairs_dict:
                messagebox.showerror("Error", "No se encontraron resultados para el rango especificado")
                return
            
            # Create notebook for tabs
            notebook = ttk.Notebook(self.range_results_frame)
            notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Tab 1: Scatter Plot
            scatter_tab = ttk.Frame(notebook)
            notebook.add(scatter_tab, text="Gráfico de Dispersión")
            
            scatter_fig = create_scatter_plot(pairs_dict)
            scatter_canvas = FigureCanvasTkAgg(scatter_fig, master=scatter_tab)
            scatter_canvas.draw()
            scatter_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Add toolbar
            scatter_toolbar = NavigationToolbar2Tk(scatter_canvas, scatter_tab)
            scatter_toolbar.update()
            
            # Tab 2: Histogram
            histogram_tab = ttk.Frame(notebook)
            notebook.add(histogram_tab, text="Histograma")
            
            histogram_fig = create_histogram(counts_dict)
            histogram_canvas = FigureCanvasTkAgg(histogram_fig, master=histogram_tab)
            histogram_canvas.draw()
            histogram_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Add toolbar
            histogram_toolbar = NavigationToolbar2Tk(histogram_canvas, histogram_tab)
            histogram_toolbar.update()
            
            # Tab 3: Data Table
            table_tab = ttk.Frame(notebook)
            notebook.add(table_tab, text="Tabla de Datos")
            
            # Create table header
            columns = ("número", "combinaciones")
            tree = ttk.Treeview(table_tab, columns=columns, show="headings")
            tree.heading("número", text="Número par")
            tree.heading("combinaciones", text="Combinaciones")
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(table_tab, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            tree.pack(fill=tk.BOTH, expand=True)
            
            # Add data to table
            for num, count in sorted(counts_dict.items()):
                tree.insert("", tk.END, values=(num, count))
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese números válidos")

if __name__ == "__main__":
    root = tk.Tk()
    app = GoldbachApp(root)
    root.mainloop()
