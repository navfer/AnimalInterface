import csv
import pandas as pd
import Animal


def readAnimal(filename, listaAnimales):
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                listaAnimales.append(Animal.Animal(row['ID'], row['Name'], row['Owner'], row['Phone'], row['Age'], row['pos']))
    except FileNotFoundError:
        print(f"File {filename} not found.")


def saveAnimal(filename, animal):
    with open(filename, 'a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([animal.ID, animal.name, animal.owner,
                         animal.phone, animal.age, animal.posFile])


def modifyAnimal(filename, animal):
    try:
        data = pd.read_csv(filename)
        row_index = data.index[data['PosFile'] == animal.posFile].tolist()

        if row_index:
            row_index = row_index[0]
            data.at[row_index, 'Name'] = animal.brand
            data.at[row_index, 'Owner'] = animal.owner
            data.at[row_index, 'Phone'] = animal.phone
            data.at[row_index, 'Age'] = animal.age

            data.to_csv(filename, index=False)
        else:
            print("Animal not found in the CSV file.")
    except pd.errors.EmptyDataError:
        print("CSV file empty.")
    except FileNotFoundError:
        print(f"File {filename} not found.")
