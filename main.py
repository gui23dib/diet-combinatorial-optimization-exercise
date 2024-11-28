import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from classes.nutrition_dataframe import NutritionDataFrame
from ant_colony_optimization import AntColonyOptimization
from genetic_algorithm_optimization import GeneticAlgorithmOptimization
from classes.food import FoodNode
from classes.nutrition_dataframe import get_csv



calories = 0
protein = 0
carbs = 0
fats = 0

food_list = get_csv('data/foods.csv')

window = tk.Tk()
window.title("Nutrition Goals")
window.geometry("1100x600")

tabControl = ttk.Notebook(window)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Main')
tabControl.add(tab2, text='Alimentos')
tabControl.add(tab3, text='Ajustes')
tabControl.pack(expand=1, fill="both")

# Add a scrollbar to tab1
canvas_tab1 = tk.Canvas(tab1)
scrollbar_tab1 = tk.Scrollbar(tab1, orient="vertical", command=canvas_tab1.yview)
scrollable_frame_tab1 = ttk.Frame(canvas_tab1)

scrollable_frame_tab1.bind(
    "<Configure>",
    lambda e: canvas_tab1.configure(
        scrollregion=canvas_tab1.bbox("all")
    )
)

canvas_tab1.create_window((0, 0), window=scrollable_frame_tab1, anchor="nw")
canvas_tab1.configure(yscrollcommand=scrollbar_tab1.set)

canvas_tab1.pack(side="left", fill="both", expand=True)
scrollbar_tab1.pack(side="right", fill="y")

# Add a scrollbar to tab2
canvas_tab2 = tk.Canvas(tab2)
scrollbar_tab2 = tk.Scrollbar(tab2, orient="vertical", command=canvas_tab2.yview)
scrollable_frame_tab2 = ttk.Frame(canvas_tab2)

scrollable_frame_tab2.bind(
    "<Configure>",
    lambda e: canvas_tab2.configure(
        scrollregion=canvas_tab2.bbox("all")
    )
)

canvas_tab2.create_window((0, 0), window=scrollable_frame_tab2, anchor="nw")
canvas_tab2.configure(yscrollcommand=scrollbar_tab2.set)

canvas_tab2.pack(side="left", fill="both", expand=True)
scrollbar_tab2.pack(side="right", fill="y")

# Add a scrollbar to tab3
canvas_tab3 = tk.Canvas(tab3)
scrollbar_tab3 = tk.Scrollbar(tab3, orient="vertical", command=canvas_tab3.yview)
scrollable_frame_tab3 = ttk.Frame(canvas_tab3)

scrollable_frame_tab3.bind(
    "<Configure>",
    lambda e: canvas_tab3.configure(
        scrollregion=canvas_tab3.bbox("all")
    )
)

canvas_tab3.create_window((0, 0), window=scrollable_frame_tab3, anchor="nw")
canvas_tab3.configure(yscrollcommand=scrollbar_tab3.set)

canvas_tab3.pack(side="left", fill="both", expand=True)
scrollbar_tab3.pack(side="right", fill="y")

def runACO():
    try:
        num_ants = int(num_ants_entry.get())
        num_iterations = int(num_iterations_entry.get())
        evaporation_rate = float(evaporation_rate_entry.get())
        alpha = float(alpha_entry.get())
        beta = float(beta_entry.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numbers for ACO settings.")
        return

    messagebox.showinfo("ACO Algorithm", "Running ACO Algorithm...")
    df = NutritionDataFrame(
        target_carbs=carbs,
        target_fat=fats,
        target_protein=protein, 
        max_calories=calories,
        foodlist=food_list
    )
    aco = AntColonyOptimization(
        problem=df,
        num_ants=num_ants,
        num_iterations=num_iterations,
        evaporation_rate=evaporation_rate,
        alpha=alpha,
        beta=beta,
    )
    best_solution, best_values, best_cal_values, best_macro_values = aco.run()
    
    plot_results(best_values, best_cal_values, best_macro_values, "ACO Algorithm Results", best_solution, df)

def runGA():
    try:
        population_length = int(population_length_entry.get())
        max_iterations = int(max_iterations_entry.get())
        solution_max_size = int(solution_max_size_entry.get())
        solution_min_size = int(solution_min_size_entry.get())
        elite_size = int(elite_size_entry.get())
        convergence_rate = float(convergence_rate_entry.get())
        mutation_rate = float(mutation_rate_entry.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numbers for GA settings.")
        return

    messagebox.showinfo("Genetic Algorithm", "Running Genetic Algorithm...")
    df = NutritionDataFrame(
        target_carbs=carbs,
        target_fat=fats,
        target_protein=protein, 
        max_calories=calories,
        foodlist=food_list
    )
    ga = GeneticAlgorithmOptimization(
        problem=df,
        population_length=population_length, 
        max_iterations=max_iterations,
        solution_max_size=solution_max_size,
        solution_min_size=solution_min_size,
        elite_size=elite_size,
        convergence_rate=convergence_rate,
        mutation_rate=mutation_rate,
    )
    best_solution, best_fit_values, best_calories_gen, best_macros_gen = ga.run()
    plot_results(best_fit_values, best_calories_gen, best_macros_gen, "Genetic Algorithm Results", best_solution, df)

def plot_results(best_values, best_cal_values, best_macro_values, title, best_solution=None, df=None):
    window.geometry("1100x800")
    fig, axs = plt.subplots(3, figsize=(10, 10))
    fig.suptitle(title, fontsize=16)

    axs[0].plot(best_values, color='green')
    axs[0].set_title('Best Values')

    axs[1].plot(best_cal_values, color='red')
    axs[1].set_title('Best Calorie Values')

    axs[2].plot([item[0] for item in best_macro_values], color='blue', label='Proteins')
    axs[2].plot([item[1] for item in best_macro_values], color='skyblue', label='Carbs')
    axs[2].plot([item[2] for item in best_macro_values], color='navy', label='Fats')
    axs[2].set_title('Best Macro Values', fontsize=14)
    axs[2].legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)
    
    fig.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.5, wspace=0.4)
        
    canvas = FigureCanvasTkAgg(fig, master=scrollable_frame_tab1)
    canvas.draw()
    canvas.get_tk_widget().grid(row=7, column=0, columnspan=2, padx=20, pady=20)
    
    if best_solution is not None and df is not None:
        listbox = tk.Listbox(scrollable_frame_tab1, font=("Helvetica", 12))
        listbox.grid(row=8, column=0, columnspan=2, rowspan=4, sticky="nsew", pady=10, padx=20)

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
            listbox.insert(tk.END, f"        Protein = {food.protein} / Carb = {food.carbs} / Fat = {food.fat}")
            
    tk.Button(scrollable_frame_tab1, text="Exit", font=("Helvetica", 14), command=window.destroy).grid(row=12, column=0, columnspan=2, pady=10, padx=20)

def show_main_page():
    global entry_calories, entry_protein, entry_carbs, entry_fats

    tk.Label(scrollable_frame_tab1, text="Calorie Objective:", font=("Helvetica", 14)).grid(row=0, column=0, pady=10)
    entry_calories = tk.Entry(scrollable_frame_tab1, font=("Helvetica", 14))
    entry_calories.grid(row=0, column=1, pady=10)
    
    tk.Label(scrollable_frame_tab1, text="Protein Goal:", font=("Helvetica", 14)).grid(row=1, column=0, pady=10)
    entry_protein = tk.Entry(scrollable_frame_tab1, font=("Helvetica", 14))
    entry_protein.grid(row=1, column=1, pady=10)
    
    tk.Label(scrollable_frame_tab1, text="Carbs Goal:", font=("Helvetica", 14)).grid(row=2, column=0, pady=10)
    entry_carbs = tk.Entry(scrollable_frame_tab1, font=("Helvetica", 14))
    entry_carbs.grid(row=2, column=1, pady=10)
    
    tk.Label(scrollable_frame_tab1, text="Fats Goal:", font=("Helvetica", 14)).grid(row=3, column=0, pady=10)
    entry_fats = tk.Entry(scrollable_frame_tab1, font=("Helvetica", 14))
    entry_fats.grid(row=3, column=1, pady=10)
    
    tk.Button(scrollable_frame_tab1, text="Confirm", command=confirm_inputs, font=("Helvetica", 14)).grid(row=4, column=0, pady=10)
    tk.Button(scrollable_frame_tab1, text="Reset", command=reset_inputs, font=("Helvetica", 14)).grid(row=4, column=1, pady=10)

def show_food_tab():
    tree = ttk.Treeview(scrollable_frame_tab2, columns=("Name", "Calories", "Protein", "Carbs", "Fat"), show="headings")
    tree.heading("Name", text="Name")
    tree.heading("Calories", text="Calories")
    tree.heading("Protein", text="Protein")
    tree.heading("Carbs", text="Carbs")
    tree.heading("Fat", text="Fat")
    tree.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

    for food in food_list:
        tree.insert("", "end", values=(food.name, food.calories, food.protein, food.carbs, food.fat))

    tk.Label(scrollable_frame_tab2, text="Name:", font=("Helvetica", 14)).grid(row=1, column=0, pady=10)
    entry_name = tk.Entry(scrollable_frame_tab2, font=("Helvetica", 14))
    entry_name.grid(row=1, column=1, pady=10)

    tk.Label(scrollable_frame_tab2, text="Calories:", font=("Helvetica", 14)).grid(row=2, column=0, pady=10)
    entry_calories_food = tk.Entry(scrollable_frame_tab2, font=("Helvetica", 14))
    entry_calories_food.grid(row=2, column=1, pady=10)

    tk.Label(scrollable_frame_tab2, text="Protein:", font=("Helvetica", 14)).grid(row=3, column=0, pady=10)
    entry_protein_food = tk.Entry(scrollable_frame_tab2, font=("Helvetica", 14))
    entry_protein_food.grid(row=3, column=1, pady=10)

    tk.Label(scrollable_frame_tab2, text="Carbs:", font=("Helvetica", 14)).grid(row=4, column=0, pady=10)
    entry_carbs_food = tk.Entry(scrollable_frame_tab2, font=("Helvetica", 14))
    entry_carbs_food.grid(row=4, column=1, pady=10)

    tk.Label(scrollable_frame_tab2, text="Fat:", font=("Helvetica", 14)).grid(row=5, column=0, pady=10)
    entry_fat_food = tk.Entry(scrollable_frame_tab2, font=("Helvetica", 14))
    entry_fat_food.grid(row=5, column=1, pady=10)

    def add_food():
        input_name = entry_name.get()
        input_calories = float(entry_calories_food.get())
        input_protein = float(entry_protein_food.get())
        input_carbs = float(entry_carbs_food.get())
        input_fat = float(entry_fat_food.get())

        if input_name and input_calories and input_protein != None and input_carbs != None and input_fat != None:
            new_food = FoodNode(input_protein, input_calories, input_fat, input_carbs, input_name)
            food_list.append(new_food)
            tree.insert("", "end", values=(input_name, input_calories, input_protein, input_carbs, input_fat))
            entry_name.delete(0, tk.END)
            entry_calories_food.delete(0, tk.END)
            entry_protein_food.delete(0, tk.END)
            entry_carbs_food.delete(0, tk.END)
            entry_fat_food.delete(0, tk.END)
        else:
            messagebox.showerror("Invalid input", "Please fill all fields.")

    tk.Button(scrollable_frame_tab2, text="Add Food", command=add_food, font=("Helvetica", 14)).grid(row=6, column=0, pady=10, padx=20)
    tk.Button(scrollable_frame_tab2, text="Delete Food", command=lambda: delete_food(tree), font=("Helvetica", 14)).grid(row=6, column=1, pady=10, padx=20)

def delete_food(tree):
    selected_item = tree.selection()[0]
    values = tree.item(selected_item, 'values')
    tree.delete(selected_item)
    
    for food in food_list:
        if (food.name, str(food.calories), str(food.protein), str(food.carbs), str(food.fat)) == values:
            food_list.remove(food)
            break

def show_settings_tab():
    global num_ants_entry, num_iterations_entry, evaporation_rate_entry, alpha_entry, beta_entry
    global population_length_entry, max_iterations_entry, solution_max_size_entry, solution_min_size_entry, elite_size_entry, convergence_rate_entry, mutation_rate_entry
    
    # ACO settings
    tk.Label(scrollable_frame_tab3, text="ACO Settings", font=("Helvetica", 16)).grid(row=0, column=0, pady=10, columnspan=2)
    
    tk.Label(scrollable_frame_tab3, text="Number of Ants:", font=("Helvetica", 14)).grid(row=1, column=0, pady=10, sticky="e")
    num_ants_entry = tk.Entry(scrollable_frame_tab3, font=("Helvetica", 14))
    num_ants_entry.insert(0, "100")
    num_ants_entry.grid(row=1, column=1, pady=10, sticky="w")

    tk.Label(scrollable_frame_tab3, text="Number of Iterations:", font=("Helvetica", 14)).grid(row=2, column=0, pady=10, sticky="e")
    num_iterations_entry = tk.Entry(scrollable_frame_tab3, font=("Helvetica", 14))
    num_iterations_entry.insert(0, "500")
    num_iterations_entry.grid(row=2, column=1, pady=10, sticky="w")

    tk.Label(scrollable_frame_tab3, text="Evaporation Rate:", font=("Helvetica", 14)).grid(row=3, column=0, pady=10, sticky="e")
    evaporation_rate_entry = tk.Entry(scrollable_frame_tab3, font=("Helvetica", 14))
    evaporation_rate_entry.insert(0, "0.6")
    evaporation_rate_entry.grid(row=3, column=1, pady=10, sticky="w")

    tk.Label(scrollable_frame_tab3, text="Alpha:", font=("Helvetica", 14)).grid(row=4, column=0, pady=10, sticky="e")
    alpha_entry = tk.Entry(scrollable_frame_tab3, font=("Helvetica", 14))
    alpha_entry.insert(0, "0.4")
    alpha_entry.grid(row=4, column=1, pady=10, sticky="w")

    tk.Label(scrollable_frame_tab3, text="Beta:", font=("Helvetica", 14)).grid(row=5, column=0, pady=10, sticky="e")
    beta_entry = tk.Entry(scrollable_frame_tab3, font=("Helvetica", 14))
    beta_entry.insert(0, "0.8")
    beta_entry.grid(row=5, column=1, pady=10, sticky="w")

    # GA settings
    tk.Label(scrollable_frame_tab3, text="GA Settings", font=("Helvetica", 16)).grid(row=0, column=2, pady=10, columnspan=2)
    
    tk.Label(scrollable_frame_tab3, text="Population Length:", font=("Helvetica", 14)).grid(row=1, column=2, pady=10, sticky="e")
    population_length_entry = tk.Entry(scrollable_frame_tab3, font=("Helvetica", 14))
    population_length_entry.insert(0, "100")
    population_length_entry.grid(row=1, column=3, pady=10, sticky="w")

    tk.Label(scrollable_frame_tab3, text="Max Iterations:", font=("Helvetica", 14)).grid(row=2, column=2, pady=10, sticky="e")
    max_iterations_entry = tk.Entry(scrollable_frame_tab3, font=("Helvetica", 14))
    max_iterations_entry.insert(0, "2500")
    max_iterations_entry.grid(row=2, column=3, pady=10, sticky="w")

    tk.Label(scrollable_frame_tab3, text="Solution Max Size:", font=("Helvetica", 14)).grid(row=3, column=2, pady=10, sticky="e")
    solution_max_size_entry = tk.Entry(scrollable_frame_tab3, font=("Helvetica", 14))
    solution_max_size_entry.insert(0, "25")
    solution_max_size_entry.grid(row=3, column=3, pady=10, sticky="w")

    tk.Label(scrollable_frame_tab3, text="Solution Min Size:", font=("Helvetica", 14)).grid(row=4, column=2, pady=10, sticky="e")
    solution_min_size_entry = tk.Entry(scrollable_frame_tab3, font=("Helvetica", 14))
    solution_min_size_entry.insert(0, "5")
    solution_min_size_entry.grid(row=4, column=3, pady=10, sticky="w")

    tk.Label(scrollable_frame_tab3, text="Elite Size:", font=("Helvetica", 14)).grid(row=5, column=2, pady=10, sticky="e")
    elite_size_entry = tk.Entry(scrollable_frame_tab3, font=("Helvetica", 14))
    elite_size_entry.insert(0, "3")
    elite_size_entry.grid(row=5, column=3, pady=10, sticky="w")

    tk.Label(scrollable_frame_tab3, text="Convergence Rate:", font=("Helvetica", 14)).grid(row=6, column=2, pady=10, sticky="e")
    convergence_rate_entry = tk.Entry(scrollable_frame_tab3, font=("Helvetica", 14))
    convergence_rate_entry.insert(0, "0.85")
    convergence_rate_entry.grid(row=6, column=3, pady=10, sticky="w")

    tk.Label(scrollable_frame_tab3, text="Mutation Rate:", font=("Helvetica", 14)).grid(row=7, column=2, pady=10, sticky="e")
    mutation_rate_entry = tk.Entry(scrollable_frame_tab3, font=("Helvetica", 14))
    mutation_rate_entry.insert(0, "0.03")
    mutation_rate_entry.grid(row=7, column=3, pady=10, sticky="w")

    tk.Button(scrollable_frame_tab3, text="Save", font=("Helvetica", 14)).grid(row=8, column=0, pady=10, padx=20, columnspan=4)

def show_pie_chart(proteintemp, carbstemp, fatstemp):
    labels = 'Protein', 'Carbs', 'Fats'
    sizes = [proteintemp, carbstemp, fatstemp]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal') 
    return fig

def confirm_inputs():
    try:
        global calories, protein, carbs, fats, canvas_pie_chart
        calories = int(entry_calories.get())
        protein = int(entry_protein.get())
        carbs = int(entry_carbs.get())
        fats = int(entry_fats.get())
        
        fig = show_pie_chart(protein, carbs, fats)
        canvas_pie_chart = FigureCanvasTkAgg(fig, master=scrollable_frame_tab1)
        canvas_pie_chart.draw()
        canvas_pie_chart.get_tk_widget().grid(row=6, columnspan=2)
        
        window.geometry("1100x800")
        
        confirm = messagebox.askyesno("Confirm Inputs", f"Calorie: {calories}\nProtein: {protein}\nCarbs: {carbs}\nFats: {fats}\n\nDo you want to proceed?")
        if confirm:
            show_algorithm_page()
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numbers for all fields.")

def reset_inputs():
    global canvas_pie_chart
    entry_calories.delete(0, tk.END)
    entry_protein.delete(0, tk.END)
    entry_carbs.delete(0, tk.END)
    entry_fats.delete(0, tk.END)
    if canvas_pie_chart:
        canvas_pie_chart.get_tk_widget().grid_forget()
        canvas_pie_chart = None

def show_algorithm_page():
    for widget in scrollable_frame_tab1.winfo_children():
        widget.destroy()
        
    tk.Label(scrollable_frame_tab1, text="Choose Algorithm:", font=("Helvetica", 16)).grid(row=0, column=0, pady=20)
    tk.Button(scrollable_frame_tab1, text="ACO Algorithm", font=("Helvetica", 14), command=runACO).grid(row=1, column=0, pady=10)
    tk.Button(scrollable_frame_tab1, text="Genetic Algorithm", font=("Helvetica", 14), command=runGA).grid(row=1, column=1, pady=10)

if __name__ == '__main__':
    show_main_page()
    show_food_tab()
    show_settings_tab()
    window.mainloop()