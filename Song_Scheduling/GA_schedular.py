import random

# Convert the harmnonic keys to a numerical value
def convert_key_to_numerical(key):
    number = int(key[:-1])
    letter = 0 if key[-1] == 'A' else 1
    return (number, letter)

# Finding the harmonic cost of the transition based on set of DJ transition rules
def calculate_harmonic_cost(key1, key2):
    num1, let1 = convert_key_to_numerical(key1)
    num2, let2 = convert_key_to_numerical(key2) 
    
    if num1 == num2 and let1 == let2:
        return 0  # Perfectly Harmonic
    elif num1 == num2 and let1 != let2:
        return 0  # Relative Major/Minor Switch
    elif let1 == let2:
        if num2 == num1 + 1 or (num1 == 12 and num2 == 1):
            return 0  # Energy Boost
        elif num2 == num1 - 1 or (num1 == 1 and num2 == 12):
            return 0  # Lower Energy
    elif let1 == 0 and let2 == 1 and num2 == num1 - 1:
        return 0  # Minor to Major Sub Dominant
    elif let1 == 1 and let2 == 0 and num2 == num1 + 1:
        return 0  # Major to Minor Sub Dominant
    
    return 20  # Any other transitions are heavily penalized 


def calculate_transition_cost(song1, song2):
    bpm_diff = abs(song1['bpm'] - song2['bpm'])
    bpm_cost = 0 if bpm_diff <= 5 else 1.5 * bpm_diff
    harmonic_cost = calculate_harmonic_cost(song1['key'], song2['key'])
    total_cost = harmonic_cost + bpm_cost
    
    return total_cost


def calculate_fitness(order, songs):
    total_cost = 0
    for i in range(len(order) - 1):
        total_cost += calculate_transition_cost(songs[order[i]], songs[order[i + 1]])
    return total_cost


def create_initial_population(songs, population_size):
    population = []
    for _ in range(population_size):
        order = list(range(len(songs)))
        random.shuffle(order)
        population.append(order)
    return population

def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    child[start:end] = parent1[start:end]
    pointer = 0
    for elem in parent2:
        if elem not in child:
            while child[pointer] is not None:
                pointer += 1
            child[pointer] = elem
    return child

def mutate(order, mutation_rate):
    for i in range(len(order)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(order) - 1)
            order[i], order[j] = order[j], order[i]
    return order

def genetic_algorithm(songs, population_size=100, generations=1000, mutation_rate=0.01):
    population = create_initial_population(songs, population_size)
    
    for generation in range(generations):
        population = sorted(population, key=lambda x: calculate_fitness(x, songs))
        next_generation = population[:population_size//2]
        
        while len(next_generation) < population_size:
            parent1, parent2 = random.sample(population[:population_size//2], 2)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            next_generation.append(child)
        
        population = next_generation
    
    best_order = min(population, key=lambda x: calculate_fitness(x, songs))
    return best_order

# Example song data with keys and BPM
songs = [
    {'title': 'Sicko Mode', 'artist': 'Travis Scott', 'bpm': 78, 'key': '1A'},
    {'title': 'God\'s Plan', 'artist': 'Drake', 'bpm': 77, 'key': '12A'},
    {'title': 'HUMBLE.', 'artist': 'Kendrick Lamar', 'bpm': 75, 'key': '11A'},
    {'title': 'Rockstar', 'artist': 'Post Malone', 'bpm': 80, 'key': '8A'},
    {'title': 'Lucid Dreams', 'artist': 'Juice WRLD', 'bpm': 84, 'key': '9A'},
    {'title': 'Money Trees', 'artist': 'Kendrick Lamar', 'bpm': 72, 'key': '10A'},
    {'title': 'XO TOUR Llif3', 'artist': 'Lil Uzi Vert', 'bpm': 155, 'key': '5A'},
    {'title': 'The Box', 'artist': 'Roddy Ricch', 'bpm': 113, 'key': '2A'},
    {'title': 'Goosebumps', 'artist': 'Travis Scott', 'bpm': 130, 'key': '6A'},
    {'title': 'Old Town Road', 'artist': 'Lil Nas X', 'bpm': 136, 'key': '7A'}
]

# For demonstration purposes, printing out the songs data
for song in songs:
    print(f"Title: {song['title']}, Artist: {song['artist']}, BPM: {song['bpm']}, Key: {song['key']}")


best_order = genetic_algorithm(songs, population_size=100, generations=1000, mutation_rate=0.01)

print("Optimal order of songs:")
for idx in best_order:
    song = songs[idx]
    print(f"Title: {song['title']}, Artist: {song['artist']}, BPM: {song['bpm']}, Key: {song['key']}")

