seating = [
    ["A1", "A2", "A3"],
    ["B1", "B2", "B3"],
    ["C1", "C2", "C3"],
]

print("Seating Chart:")
for row in seating:
    print(" ".join(row))

print("\n"+seating[1][0])

print("\n"+seating[-1][-1])