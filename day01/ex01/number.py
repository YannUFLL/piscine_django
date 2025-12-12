def main():
    numbers_list =  extract_numbers()
    for number in numbers_list: 
        print(number)


def extract_numbers():
    try:
        with open("numbers.txt", "r") as file:
            numbers_list = file.read().strip().split(",")
            return numbers_list
    except FileNotFoundError:
        print("File not found")

if __name__ == "__main__":
    main()