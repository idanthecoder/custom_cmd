

def main():
    run = True

    while run:
        word = input("pls enter inputs:\n")
        print(f"first letter of word: {word[0]}")

        if word == "exit":
            run = False
            print("end of scripts")


if __name__ == '__main__':
    main()
