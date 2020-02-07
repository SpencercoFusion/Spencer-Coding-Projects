import math as m
import random as rand

''''''
def get_distance(point):
    x1 = point[0]
    y1 = point[1]
    distance = m.sqrt( (x1)**2 + (y1)**2 )
    return distance
def chord_length(distance, radius):
    if (distance <= radius):
        chord_length = 2 * m.sqrt( (radius)**2 - (distance)**2 )
        return chord_length
    else:
        return False

''''''
square_length = 1
resolution = 10**6
radius = square_length/2

average = 0
for i in range(1000):
    print()
    radius = square_length/2
    x = rand.randrange(-resolution/2, resolution/2)/resolution
    y = rand.randrange(-resolution/2, resolution/2)/resolution

    wins = 1
    losses = 0
    while (losses < 1):
        d = get_distance((x,y))
        if(d <= radius):
            chord = chord_length(d, radius)
            radius = chord/2
            wins += 1

        else:
            losses = 1
        print("distance: " + str(d))
        print("radius: " + str(radius))
        print()
        
    average = (average * (i) + wins)/(i + 1)
    print("round " + str(i+1) + " -wins: " + str(wins))
print()
print("average: " + str(average))


