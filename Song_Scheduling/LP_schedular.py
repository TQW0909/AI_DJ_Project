import numpy as np

# Convert the harmonic keys to a numerical value
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
    
    return 10  # Any other transitions are heavily penalized 

def calculate_transition_cost(bpm1, bpm2, key1, key2):
    bpm_diff = abs(bpm1 - bpm2)
    bpm_cost = 0 if bpm_diff <= 5 else 15 * bpm_diff
    harmonic_cost = calculate_harmonic_cost(key1, key2)
    total_cost = harmonic_cost + bpm_cost
    
    return total_cost

def optimal_mix_order(bpm_list, key_list):
    n = len(bpm_list)
    dp = [[float('inf')] * n for _ in range(1 << n)]
    path = [[-1] * n for _ in range(1 << n)]

    # Base case: starting with each song
    for i in range(n):
        dp[1 << i][i] = 0

    # Fill the DP table
    for mask in range(1 << n):
        for i in range(n):
            if mask & (1 << i):
                for j in range(n):
                    if mask & (1 << j) == 0:
                        next_mask = mask | (1 << j)
                        cost = dp[mask][i] + calculate_transition_cost(bpm_list[i], bpm_list[j], key_list[i], key_list[j])
                        if cost < dp[next_mask][j]:
                            dp[next_mask][j] = cost
                            path[next_mask][j] = i

    # Find the minimum cost and corresponding ending song
    min_cost = float('inf')
    end_song = -1
    final_mask = (1 << n) - 1
    for i in range(n):
        if dp[final_mask][i] < min_cost:
            min_cost = dp[final_mask][i]
            end_song = i

    # Trace back the optimal path
    optimal_order = []
    current_song = end_song
    current_mask = final_mask
    while current_song != -1:
        optimal_order.append(current_song)
        next_song = path[current_mask][current_song]
        current_mask &= ~(1 << current_song)
        current_song = next_song

    optimal_order.reverse()
    return optimal_order, min_cost

def LP_sched(bpm_list, key_list):
    optimal_order, min_cost = optimal_mix_order(bpm_list, key_list)
    print(f"Minimum transition cost: {min_cost}")
    return optimal_order

# # Example data
# bpm_list = [78, 77, 75, 80, 84, 72, 155, 113, 130, 136]
# key_list = ['1A', '12A', '11A', '8A', '9A', '10A', '5A', '2A', '6A', '7A']

# # Get the optimal mix order

# # Output the optimal order of songs
# print("Optimal order of songs:")
# for idx in optimal_order:
#     print(f"Song {idx + 1} (BPM: {bpm_list[idx]}, Key: {key_list[idx]})")

# print(f"Minimum transition cost: {min_cost}")
