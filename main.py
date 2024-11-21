import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ant_colony.nutrition_dataframe import NutritionDataFrame
from ant_colony.ant_colony_optimization import AntColonyOptimization

global calories, protein, carbs, fats

calories = 0
protein = 0
carbs = 0
fats = 0

entry_calories = None
entry_protein = None
entry_carbs = None
entry_fats = None

window = tk.Tk()
window.title("Nutrition Goals")

def runACO():
    messagebox.showinfo("ACO Algorithm", "Running ACO Algorithm...")
    df = NutritionDataFrame(target_macro=protein, max_calories=calories)
    aco = AntColonyOptimization(
        problem=df,
        num_ants=100,
        num_iterations=500,
        evaporation_rate=0.6,
        alpha=0.4,
        beta=0.8,
    )
    best_solution, best_value, best_values, best_cal_values = aco.run()
    plot_results(best_values, best_cal_values, "ACO Algorithm Results", best_solution, best_value, df)

def runGA():
    messagebox.showinfo("Genetic Algorithm", "Running Genetic Algorithm...")
    # Assuming similar structure for GA
    best_values = [1, 2, 3, 4, 5]  # Replace with actual GA results
    best_cal_values = [5, 4, 3, 2, 1]  # Replace with actual GA results
    plot_results(best_values, best_cal_values, "Genetic Algorithm Results")

def plot_results(best_values, best_cal_values, title, best_solution=None, best_value=None, df=None):
    window.geometry("800x1000")
    fig, axs = plt.subplots(2)
    fig.suptitle(title)
    
    axs[0].plot(best_values, color='green')
    axs[0].set_title('Best Values')
    
    axs[1].plot(best_cal_values, color='red')
    axs[1].set_title('Best Calorie Values')
    
    fig.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.4, wspace=0.4)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=7, columnspan=2)
    
    if best_solution is not None and best_value is not None and df is not None:
        listbox = tk.Listbox(window, font=("Helvetica", 12))
        listbox.grid(row=8, column=0, columnspan=2, rowspan=4, sticky="nsew", pady=10)

        food_counts = {}
        for i in best_solution:
            food = df.foodlist[i]
            if food.name in food_counts:
                food_counts[food.name]['count'] += 1
            else:
                food_counts[food.name] = {'food': food, 'count': 1}

        for _, data in food_counts.items():
            food = data['food']
            count = data['count']
            listbox.insert(tk.END, f"{count}x - {food.name}:")
            listbox.insert(tk.END, f"        Calories = {food.calories}")
            listbox.insert(tk.END, f"        Protein = {food.protein}")
    
    tk.Button(window, text="Exit", font=("Helvetica", 14), command=window.destroy).grid(row=12, columnspan=2, pady=10)

def show_main_page():
    for widget in window.winfo_children():
        widget.destroy()
    
    tk.Label(window, text="Calorie Objective:", font=("Helvetica", 14)).grid(row=0, column=0, pady=10)
    entry_calories.grid(row=0, column=1, pady=10)
    
    tk.Label(window, text="Protein Goal:", font=("Helvetica", 14)).grid(row=1, column=0, pady=10)
    entry_protein.grid(row=1, column=1, pady=10)
    
    tk.Label(window, text="Carbs Goal:", font=("Helvetica", 14)).grid(row=2, column=0, pady=10)
    entry_carbs.grid(row=2, column=1, pady=10)
    
    tk.Label(window, text="Fats Goal:", font=("Helvetica", 14)).grid(row=3, column=0, pady=10)
    entry_fats.grid(row=3, column=1, pady=10)
    
    tk.Button(window, text="Confirm", command=confirm_inputs, font=("Helvetica", 14)).grid(row=4, column=0, pady=10)
    tk.Button(window, text="Reset", command=reset_inputs, font=("Helvetica", 14)).grid(row=4, column=1, pady=10)

def show_pie_chart(protein, carbs, fats):
    labels = 'Protein', 'Carbs', 'Fats'
    sizes = [protein, carbs, fats]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal') 
    return fig

def confirm_inputs():
    try:
        global calories, protein, carbs, fats
        calories = int(entry_calories.get())
        protein = int(entry_protein.get())
        carbs = int(entry_carbs.get())
        fats = int(entry_fats.get())
        
        fig = show_pie_chart(protein, carbs, fats)
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().grid(row=6, columnspan=2)
        
        window.geometry("800x600")
        
        confirm = messagebox.askyesno("Confirm Inputs", f"Calorie: {calories}\nProtein: {protein}\nCarbs: {carbs}\nFats: {fats}\n\nDo you want to proceed?")
        if confirm:
            show_algorithm_page()
        show_algorithm_page()
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numbers for all fields.")

def reset_inputs():
    entry_calories.delete(0, tk.END)
    entry_protein.delete(0, tk.END)
    entry_carbs.delete(0, tk.END)
    entry_fats.delete(0, tk.END)

def show_algorithm_page():
    for widget in window.winfo_children():
        widget.destroy()
        
    tk.Label(window, text="Choose Algorithm:", font=("Helvetica", 16)).grid(row=0, column=0, pady=20)
    tk.Button(window, text="ACO Algorithm", font=("Helvetica", 14), command=runACO).grid(row=1, column=0, pady=10)
    tk.Button(window, text="Genetic Algorithm", font=("Helvetica", 14), command=runGA).grid(row=1, column=1, pady=10)
        

if __name__ == '__main__':
    tk.Label(window, text="Calorie Objective:", font=("Helvetica", 14)).grid(row=0, column=0, pady=10)
    entry_calories = tk.Entry(window, font=("Helvetica", 14))
    entry_calories.grid(row=0, column=1, pady=10)

    tk.Label(window, text="Protein Goal:", font=("Helvetica", 14)).grid(row=1, column=0, pady=10)
    entry_protein = tk.Entry(window, font=("Helvetica", 14))
    entry_protein.grid(row=1, column=1, pady=10)

    tk.Label(window, text="Carbs Goal:", font=("Helvetica", 14)).grid(row=2, column=0, pady=10)
    entry_carbs = tk.Entry(window, font=("Helvetica", 14))
    entry_carbs.grid(row=2, column=1, pady=10)

    tk.Label(window, text="Fats Goal:", font=("Helvetica", 14)).grid(row=3, column=0, pady=10)
    entry_fats = tk.Entry(window, font=("Helvetica", 14))
    entry_fats.grid(row=3, column=1, pady=10)

    tk.Button(window, text="Confirm", command=confirm_inputs, font=("Helvetica", 14)).grid(row=4, column=0, pady=10)
    tk.Button(window, text="Reset", command=reset_inputs, font=("Helvetica", 14)).grid(row=4, column=1, pady=10)

    window.mainloop()