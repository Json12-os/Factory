import spolocneVariables
file = open(f"saves/{spolocneVariables.saveName}/world/0_0.txt", "r")
regio = [arr.strip().split(";") for arr in file.readlines()]
print(regio)
