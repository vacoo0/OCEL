import re
import re

text = """

'\n\nStep 1: Action: Making; Objects: Cosmopolitan; Start: 0.719 
    \nStep 2: Action: Adding; Objects: Vodka, Cointreau, Lime Juice, Cranberry Juice; Start: 4.56
    \nStep 3: Action: Shaking; Objects: Cocktail; Start: 7.02
    \nStep 4: Action: Straining; Objects: Cocktail; Start: 20.64
    \nStep 5: Action: Pouring; Objects: Cocktail; Start: 29.58
    \nStep 6: Action: Garnishing; Objects: Cocktail; Start: 34.2' 
"""

def extracting_gpt(text):
    pattern = r"Step \d+:.+?(?=n?Step \d+|$)"
    matches = re.findall(pattern, text, re.DOTALL)

    steps = [match.strip() for match in matches]
    obj = []
    action = []
    start = []

    for i in steps:
        objects = []
        pattern = r"Objects: (.+?);"
        matches = re.findall(pattern, i)

        if matches:
            objects = [obj.strip() for obj in matches[0].split(',')]
            obj.append(objects)
        else:
            obj.append([None])

        pattern2 = r"Action: (.+?);"
        matches2 = re.findall(pattern2, i)
        if matches2:
            one_action = matches2[0].strip()
            # print(one_action)
            action.append(one_action)
        else:
            action.append(None)

        start_pattern = r"Start: ([0-9.]+)"
        start_match = re.search(start_pattern, i)

        if start_match:
            time = round(float(start_match.group(1)),2)
            start.append(time)
        else:
            action.append(start)


    return obj, action, start

# obj, action, start = extracting_gpt(text)
# print(obj)
# print(action)
# print(start)
