# used to format csv files for presets
name = "output.csv"
file = open(name, "r")
cells = []
for line in file:
    a,b = line.split(",")
    cells.append([int(a),int(b)])
file.close()
itemname = input("Enter structure name:")
print(f'"{itemname}": {cells}')