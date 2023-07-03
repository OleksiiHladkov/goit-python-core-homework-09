contacts = {}


def split_string(value:str) -> list:
    result = []
    
    lst = value.split(" ")
    
    if len(lst) >= 2:
        if (lst[0] == "good" and lst[1] == "bye") or (lst[0] == "show" and lst[1] == "all"):
            result.append(lst[0] + " " + lst[1])
        else:
            result = lst.copy()
    else:
        result = lst.copy()

    return result


def command_hello(string:str) -> tuple:
    lst = split_string(string)
    
    if lst[0] == "hello":
        return "hello", "How can I help you?"
    else:
        return "", ""


def command_add(string:str) -> tuple:
    lst = split_string(string)
    
    if lst[0] == "add":
        contact = lst[1]
        number = lst[2]
        contacts[contact] = number
        return "success", f"Successfully added contact \"{contact}\" with number \"{number}\""
    else:
        # return "false", f"Sorry, can't add contact \"{contact}\" with number \"{number}\""
        return "false", ""
    

def command_change(string:str) -> tuple:
    lst = split_string(string)

    if lst[0] == "change":
        contact = lst[1]
        number = lst[2]
        contacts[contact] = number
        return "success", f"Successfully changed contact \"{contact}\" with number \"{number}\""
    else:
        # return "false", f"Sorry, can't chang contact \"{contact}\" with number \"{number}\""
        return "false", ""
    

def command_phone(string:str) -> tuple:
    lst = split_string(string)

    if lst[0] == "phone":
        contact = lst[1]
        number = contacts.get(contact)
        return "success", f"Successfully finded number \"{number}\" by contact \"{contact}\""
    else:
        # return "false", f"Sorry, can't find number by contact \"{contact}\""
        return "false", ""


def command_show_all(string:str) -> tuple:
    lst = split_string(string)
    
    if lst[0] == "show all":
        result = ""
        for contact, number in contacts.items():
            result += f"{contact}: {number}\n"
        return "success", result
    else:
        return "", ""


def command_exit(string:str) -> tuple:
    lst = split_string(string)
    
    if lst[0] == "exit" or lst[0] == "good bye" or lst[0] == "close":
        return "exit", "Good bye!"
    else:
        return "", ""


COMMANDS = {"hello": command_hello,
            "add": command_add,
            "change": command_change,
            "phone": command_phone,
            "show all": command_show_all,
            "good bye": command_exit,
            "close": command_exit,
            "exit": command_exit,}


def get_handler(command:str):
    lst = split_string(command)
    return COMMANDS[lst[0]]


def main():
    while True:
        user_input = input("Enter command: ").lower()
        
        handler = get_handler(user_input)
        result = handler(user_input)
        
        if result[0] == "exit":
            print(result[1])
            break

        print(result[1])     




if __name__ == "__main__":
    main()
    # print(contacts)