

def main():
    run = True

    while run:
        word = input("pls enter input:\n")
        print(f"you wrote: {word}")

        if word == "exit":
            run = False
            print("end of script")


if __name__ == '__main__':
    main()
