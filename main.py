import re

contacts = {}


def parcing_data(value:str) -> dict:
    result = {"command": ""}

    find_command = False
    count = 1
    start = 0
    
    for lit in value:
        
        is_finish = (count == len(value))
        first_coundition = (lit == " " or is_finish)
        second_coundition = (lit.isnumeric() or lit == "+")
        
        chunk = value[start:count].strip()
        
        if first_coundition and not find_command:
            
            if chunk in tuple(COMMANDS.keys()):
                find_command = True
                result["command"] = chunk
                start = count
        elif (second_coundition or is_finish) and find_command:
            if is_finish:
                if chunk:
                    result["name"] = chunk
            else:
                if chunk[:-1].strip():
                    result["name"] = chunk[:-1].strip()
                if value[count-1:len(value)]:
                    result["phone"] = value[count-1:len(value)]
            break

        count += 1

    return result


def chek_phone(phone):
    result = re.findall(
        r"(\+\d{1,3}\(\d{2}\)\d{3}\-(?:\d{2}\-\d{2}|\d{1}\-\d{3}))", phone)
    return result == list()


def input_error(handler_func):
    def inner_func(**kwargs):
        try:
            result = handler_func(**kwargs)
            
            value_error_types = ""
            command = kwargs["command"]
            name = kwargs["name"]
            phone = kwargs["phone"]
            
            if command == "add":
                if name in tuple(contacts.keys()):
                    value_error_types = "name_find"
                    raise ValueError()
            
            if command == "change" or command == "phone":
                if not name in tuple(contacts.keys()):
                    value_error_types = "name_not_find"
                    raise ValueError()

            if command == "add" or command == "change":
                if phone in tuple(contacts.values()):
                    value_error_types = "phone_find"
                    raise ValueError()
                
                if chek_phone(kwargs["phone"]):
                    value_error_types = "phone_format"
                    raise ValueError()

        except KeyError as key:
            result = "failure", f"You must enter {key}"
        except ValueError:
            if value_error_types == "phone_format":
                result = "failure", "Phone number must be in format '+[country code]([town code])[number]'. For example: '+380(66)111-1-111' or '+380(66)111-11-11'"
            if value_error_types == "name_find":
                result = "failure", f"Name '{name}' is already use"
            if value_error_types == "phone_find":
                result = "failure", f"Phone '{phone}' is already use"
            if value_error_types == "name_not_find":
                result = "failure", f"Name '{name}' is not find"

        return result
    return inner_func


def command_hello(**kwargs) -> tuple:
    return "hello", "How can I help you?"


@input_error
def command_add(**kwargs) -> tuple:
    name = kwargs["name"]
    phone = kwargs["phone"]
    contacts[name] = phone
    return "success", f"Successfully added contact '{name}' with number '{phone}'"


@input_error
def command_change(**kwargs) -> tuple:
    name = kwargs["name"]
    phone = kwargs["phone"]
    contacts[name] = phone
    return "success", f"Successfully changed contact '{name}' with number '{phone}'"
    

@input_error
def command_phone(**kwargs) -> tuple:
    name = kwargs["name"]
    phone = contacts.get(name)
    
    if phone:
        return "success", f"Successfully finded number '{phone}' by contact '{name}'"
    else:
        return "failure", ""


def command_show_all(**kwargs) -> tuple:
    result = ""
    
    for name, phone in contacts.items():
        result += f"{name}: {phone}\n"
    
    if result:
        return "success", result
    else:
        return "failure", result


def command_exit(**kwargs) -> tuple:
    return "exit", "Good bye!"


COMMANDS = {"hello": command_hello,
            "add": command_add,
            "change": command_change,
            "phone": command_phone,
            "show all": command_show_all,
            "good bye": command_exit,
            "close": command_exit,
            "exit": command_exit,}


def get_handler(command:str):
    return COMMANDS[command.lower()]


def main():
    while True:
        user_input = input("Enter command: ")
        
        command_dict = parcing_data(user_input)

        command = command_dict.get("command", "")
        
        if command:
            handler = get_handler(command)        
            result = handler(**command_dict)
            
            if result[0] == "exit":
                print(result[1])
                break

            print(result[1])
        else:
            print("Can not recognize a command! Please, try again.")     




if __name__ == "__main__":
    main()
    