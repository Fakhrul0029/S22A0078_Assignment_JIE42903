# TV Program Scheduling using Genetic Algorithm and Streamlit Interface 

import streamlit as st
import pandas as pd
import random

st.title("TV Program Scheduling using Genetic Algorithm")

# Load dataset
st.subheader("Program Ratings Dataset")

file_path = "program_ratings(modified).csv" 
df = pd.read_csv(file_path)
st.success("Dataset loaded")
st.dataframe(df)

# Convert dataset to readable
program_ratings = {}
for _, row in df.iterrows():
    program = row.iloc[0]
    ratings = list(row.iloc[1:].values)
    program_ratings[program] = ratings

all_programs = list(program_ratings.keys())
all_time_slots = list(range(6, 6 + len(df.columns) - 1))


# Genetic algorithm core
def fitness_function(schedule):
    """Calculate total rating for a schedule."""
    total_rating = 0
    for time_slot, program in enumerate(schedule):
        total_rating += program_ratings[program][time_slot]
    return total_rating

def crossover(schedule1, schedule2):
    """Single-point crossover."""
    crossover_point = random.randint(1, len(schedule1) - 2)
    child1 = schedule1[:crossover_point] + schedule2[crossover_point:]
    child2 = schedule2[:crossover_point] + schedule1[crossover_point:]
    return child1, child2

def mutate(schedule):
    """Randomly replace one program in the schedule."""
    mutation_point = random.randint(0, len(schedule) - 1)
    new_program = random.choice(all_programs)
    schedule[mutation_point] = new_program
    return schedule

def genetic_algorithm(generations, population_size, crossover_rate, mutation_rate):
    """Run the GA optimization."""
    population = [random.sample(all_programs, len(all_programs)) for _ in range(population_size)]

    for _ in range(generations):
        population.sort(key=fitness_function, reverse=True)
        new_population = []

        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population, k=2)

            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1.copy(), parent2.copy()

            if random.random() < mutation_rate:
                child1 = mutate(child1)
            if random.random() < mutation_rate:
                child2 = mutate(child2)

            new_population.extend([child1, child2])

        population = new_population[:population_size]

    best_schedule = max(population, key=fitness_function)
    best_fitness = fitness_function(best_schedule)
    return best_schedule, best_fitness


# Streamlit interface
st.subheader("Genetic Algorithm Parameters")

# Trial 1
st.markdown("Trial 1")
co1 = st.slider("Crossover Rate (Trial 1)", 0.0, 0.95, 0.8, step=0.01, key="co1")
mut1 = st.slider("Mutation Rate (Trial 1)", 0.01, 0.05, 0.02, step=0.01, key="mut1")

# Trial 2
st.markdown("Trial 2")
co2 = st.slider("Crossover Rate (Trial 2)", 0.0, 0.95, 0.7, step=0.01, key="co2")
mut2 = st.slider("Mutation Rate (Trial 2)", 0.01, 0.05, 0.03, step=0.01, key="mut2")

# Trial 3
st.markdown("Trial 3")
co3 = st.slider("Crossover Rate (Trial 3)", 0.0, 0.95, 0.9, step=0.01, key="co3")
mut3 = st.slider("Mutation Rate (Trial 3)", 0.01, 0.05, 0.05, step=0.01, key="mut3")

generations = st.number_input("Generations", 10, 500, 100)
pop_size = st.number_input("Population Size", 10, 200, 50)


# Run and display results
if st.button("Run All 3 Trials"):
    trial_params = [(co1, mut1), (co2, mut2), (co3, mut3)]

    for i, (co, mut) in enumerate(trial_params, start=1):
        st.divider()
        st.markdown(f"## 🔹 Trial {i}: CO_R = {co}, MUT_R = {mut}")

        best_schedule, best_fitness = genetic_algorithm(generations, pop_size, co, mut)

        results = []
        for hour, program in zip(all_time_slots, best_schedule):
            results.append({
                "Hour": f"{hour}:00",
                "Program": program,
                "Ratings": program_ratings[program][hour - 6]
            })

        result_df = pd.DataFrame(results)
        st.dataframe(result_df)
        st.success(f"Best Fitness (Total Ratings): {best_fitness}")

        # Save each trial result for documentation
        result_df.to_csv(f"trial_{i}_tv_schedule.csv", index=False)

st.info("Adjust the crossover and mutation rates above to observe their impact on total ratings performance.")



