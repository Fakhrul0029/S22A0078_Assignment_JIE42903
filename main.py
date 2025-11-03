# University Exam Scheduling using Genetic Algorithm and Streamlit Interface 

import streamlit as st
import pandas as pd
import random

# Load dataset
@st.cache_data
def load_dataset(file_path):
    df = pd.read_csv(file_path)
    return df

st.title("University Exam Scheduling using Genetic Algorithm")

uploaded_file = st.file_uploader("Upload classroom CSV file", type=["csv"])

if uploaded_file:
    df = load_dataset(uploaded_file)
    st.success("Dataset loaded successfully")
    st.dataframe(df.head())
else:
    st.warning("Please upload your CSV dataset to proceed")
    st.stop()

# Creation of example exam data
exams = [
    {"name": "Mathematics", "students": 40, "type": "Lecture Hall"},
    {"name": "Artificial Intelligence", "students": 30, "type": "Lab"},
    {"name": "Digital Business", "students": 25, "type": "Classroom"},
    {"name": "Software Engineering", "students": 35, "type": "Lecture Hall"},
    {"name": "Networking", "students": 28, "type": "Lab"},
    {"name": "Cybersecurity", "students": 38, "type": "Lab"},
    {"name": "Database Systems", "students": 32, "type": "Classroom"},
    {"name": "Statistics", "students": 45, "type": "Lecture Hall"},
    {"name": "Entrepreneurship", "students": 26, "type": "Classroom"},
    {"name": "Machine Learning", "students": 33, "type": "Lab"},
]

# Fitness function
def fitness_function(schedule):
    total_score = 0
    for exam, classroom in zip(exams, schedule):
        room_capacity = classroom['capacity']
        room_type = classroom['room_type']

        # Penalize overcapacity
        if exam['students'] > room_capacity:
            total_score -= (exam['students'] - room_capacity) * 2
        else:
            total_score += exam['students']

        # Reward correct room type match
        if exam['type'] == room_type:
            total_score += 10
        elif exam['type'] in room_type:  # partial match
            total_score += 5
        else:
            total_score -= 5

    return total_score

# Core GA functions
def create_random_schedule(df):
    return random.sample(df.to_dict('records'), len(exams))

def initialize_population(df, pop_size):
    return [create_random_schedule(df) for _ in range(pop_size)]

def crossover(parent1, parent2):
    point = random.randint(1, len(exams) - 2)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(schedule):
    i, j = random.sample(range(len(schedule)), 2)
    schedule[i], schedule[j] = schedule[j], schedule[i]
    return schedule

def genetic_algorithm(df, generations, pop_size, co_rate, mut_rate, elitism):
    population = initialize_population(df, pop_size)

    for _ in range(generations):
        scored = [(fitness_function(s), s) for s in population]
        scored.sort(reverse=True, key=lambda x: x[0])

        new_population = [s for _, s in scored[:elitism]]

        while len(new_population) < pop_size:
            parent1, parent2 = random.choices(population, k=2)
            if random.random() < co_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1[:], parent2[:]

            if random.random() < mut_rate:
                child1 = mutate(child1)
            if random.random() < mut_rate:
                child2 = mutate(child2)

            new_population.extend([child1, child2])

        population = new_population[:pop_size]

    best_schedule = max(population, key=lambda s: fitness_function(s))
    best_fitness = fitness_function(best_schedule)
    return best_schedule, best_fitness

# Streamlit interface for GA parameters

st.subheader("⚙️ Genetic Algorithm Parameters")

# Trial 1
st.markdown("### 🧪 Trial 1 Parameters")
co1 = st.slider("Crossover Rate (Trial 1)", 0.0, 0.95, 0.8, step=0.01, key="co1")
mut1 = st.slider("Mutation Rate (Trial 1)", 0.01, 0.05, 0.02, step=0.01, key="mut1")

# Trial 2
st.markdown("### 🧪 Trial 2 Parameters")
co2 = st.slider("Crossover Rate (Trial 2)", 0.0, 0.95, 0.7, step=0.01, key="co2")
mut2 = st.slider("Mutation Rate (Trial 2)", 0.01, 0.05, 0.03, step=0.01, key="mut2")

# Trial 3
st.markdown("### 🧪 Trial 3 Parameters")
co3 = st.slider("Crossover Rate (Trial 3)", 0.0, 0.95, 0.9, step=0.01, key="co3")
mut3 = st.slider("Mutation Rate (Trial 3)", 0.01, 0.05, 0.05, step=0.01, key="mut3")

generations = st.number_input("Generations", 10, 500, 100)
pop_size = st.number_input("Population Size", 10, 200, 50)
elitism = st.number_input("Elitism Size", 1, 10, 2)

# Run and display results
if st.button("🚀 Run All 3 Trials"):
    trial_params = [(co1, mut1), (co2, mut2), (co3, mut3)]
    for i, (co, mut) in enumerate(trial_params, start=1):
        st.divider()
        st.markdown(f"## 🔹 Trial {i}: CO_R = {co}, MUT_R = {mut}")

        best_schedule, best_fitness = genetic_algorithm(df, generations, pop_size, co, mut, elitism)

        results = []
        for exam, classroom in zip(exams, best_schedule):
            results.append({
                "Exam": exam['name'],
                "Students": exam['students'],
                "Preferred Room Type": exam['type'],
                "Assigned Room": f"{classroom['building_name']}-{classroom['room_number']}",
                "Room Type": classroom['room_type'],
                "Room Capacity": classroom['capacity']
            })

        result_df = pd.DataFrame(results)
        st.dataframe(result_df)
        st.success(f"Best Fitness Score: {best_fitness}")

        # save result for documentation
        result_df.to_csv(f"trial_{i}_result.csv", index=False)

st.info("Adjust the parameters above to experiment and observe how crossover and mutation rates affect scheduling efficiency")
