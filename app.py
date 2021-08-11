def fizzbuzz():
    selected_number = input("Select a number: ")
    if int(selected_number)%3 ==0 and int(selected_number)%5 == 0:
        print("FizzBuzz")
    elif int(selected_number)%3 ==0:
       print("Fizz")
    elif int(selected_number)%5 == 0:
        print("Buzz")
    else:
        print(f"{selected_number} is NOT divisble by both 5 and 3")


fizzbuzz()
    
