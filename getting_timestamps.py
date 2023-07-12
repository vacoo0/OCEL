import re
text = '''\n\n[Step 1: Object - Cocktail Shaker, Action - add, Start - 0.719], \n[Step 2: Object - Vodka, Action - pour, Start - 4.56], \n[Step 3: Object - Cointreau, Action - pour, Start - 7.02],\n[Step 4: Object - Lime Juice, Action - pour, Start - 9.72], \n[Step 5: Object - Cranberry Juice, Action - pour, Start - 12.12], \n[Step 6: Object - Ice, Action - add, Start - 16.379],\n[Step 7: Object - Cocktail Shaker, Action - shake, Start - 20.64],\n[Step 8: Object - Cocktail Shaker, Action - double strain, Start - 29.58],\n[Step 9: Object - Cocktail Glass, Action - fill, Start - 31.26], \n[Step 10: Object - Lemon Peel, Action - garnish, Start - 34.2].'''

timestamps = re.findall(r"Start - (\d+)", text)

# Convert timestamps to floats
timestamps = [int(ts) for ts in timestamps]

print("Rounded Timestamps:", timestamps)