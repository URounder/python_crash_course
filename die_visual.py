from die import Die

# create a D6
die = Die()

# Make some rolls, and store the results in a list
results = []
for roll_num in range(10000):
    result = die.roll()
    results.append(result)

# Analyze results
frequencies = []
for value in range(1, die.num_sides+1):
    frequency = results.count(value)
    frequencies.append(frequency)

print(frequencies)
