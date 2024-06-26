import numpy as np

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


def optimal_mix_order(songs):
    n = len(songs)
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
                        cost = dp[mask][i] + calculate_transition_cost(songs[i], songs[j])
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

    # Output the optimal order of songs
    print("Optimal order of songs:")
    for idx in optimal_order:
        song = songs[idx]
        print(f"Title: {song['title']}, Artist: {song['artist']}, BPM: {song['bpm']}, Key: {song['key']}")

    print(f"Minimum transition cost: {min_cost}")

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


optimal_mix_order(songs)
