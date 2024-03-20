import csv

if __name__ == "__main__":
    chart = []
    with open("winrates.csv", 'r') as file:
        chart = list(csv.reader(file))
    print(chart)
    names = chart[0]
    playrates = chart[1]
    chart = chart[2:]
    name = input("What Name?:\n>> ").upper()
    index = names.index(name)
    assert name in names
    del names[index]
    del playrates[index]
    del chart[index]
    for item in chart[index:]:
        del item[index]

    with open("winrates.csv", 'w') as file:
        file.write(','.join(names)+'\n')
        file.write(','.join(playrates)+'\n')
        for line_list in chart:
            file.write(','.join(line_list)+'\n')