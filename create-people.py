import random
import string
import csv

first_names = ["Ana", "Bruno", "Carlos", "Daniela", "Eduardo", "Fernanda", "Gabriel", "Helena", "Igor", "Juliana"]
last_names = ["Silva", "Santos", "Oliveira", "Pereira", "Costa", "Almeida", "Ribeiro", "Martins", "Barbosa", "Rocha"]
departments = ["Recursos Humanos", "Finanças", "Engenharia", "Marketing", "Vendas"]
supervisors = ["Supervisor A", "Supervisor B", "Supervisor C", "Supervisor D", "Supervisor E"]

used_codes = set()

def generate_unique_code():
    while True:
        code = ''.join(random.choices(string.digits, k=4))
        if code not in used_codes:
            used_codes.add(code)
            return code

def generate_person():
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    code = generate_unique_code()
    department = random.choice(departments)
    supervisor = random.choice(supervisors)
    return f"{first_name} {last_name}, Code: {code}, Department: {department}, Supervisor: {supervisor}"

if __name__ == "__main__":
    for _ in range(50):
        print(generate_person())
        with open('/home/br4b0/Desktop/novo_lar/bergamoto/people.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Fname", "Lname", "Code", "Department", "Supervisor"])
            for _ in range(50):
                person = generate_person().split(", ")
                first_name, last_name = person[0].split(" ")
                code = person[1].split(": ")[1]
                department = person[2].split(": ")[1]
                supervisor = person[3].split(": ")[1]
                writer.writerow([first_name, last_name, code, department, supervisor])