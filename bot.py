import sys, re


class NameArgumentError(Exception):
    pass


class PhoneArgumentError(Exception):
    pass


def input_error(func):
    def inner(*a,**k):
        try:
            return func(*a,**k)
        except TypeError:
            return "You entered a wrong number of arguments, try again"
        except IndexError:
            return "You entered wrong index, try again"
        except ValueError:
            return "You entered wrong nuber of arguments, try again"
        except KeyError:
            return "Unknown command. Type 'help' to show a list of commands"
        except NameArgumentError:
            return "Wrong name format, try again. The name can contain only letters of the Latin alphabet"
        except PhoneArgumentError:
            return "Wrong phone format, try again. A phone number can only contain numbers and a '+' at the beginning"
    return inner


def main():
    print(info())
    while True:
        main_input = input("Input command: ")
        body = parser(main_input)
        if type(body) == list:
            func = body[0](body[1], body[2])
            print(func)
        else:
            print(body)


@input_error
def parser(string):
    string = string.lower()
    string = re.sub(f"^ +", '', string)
    com = ""
    first = ""
    second = ""
    flag = True
    for key, value in commands.items():
        if re.search(key, string):
            com = value
            if string != key:
                without_key = re.sub(key, '', string).removeprefix(' ')
                first = without_key.split()[0]
                if without_key != first:
                    second = without_key.split()[1].removeprefix('+')
            flag = False
            break
    if flag:
        raise KeyError
    return [com, first, second]


#   -----handler's-----
def hello(*args,**kwargs):
    return "Hi, how can i help you? You can type 'help' to show a list of commands"

@input_error
def add(name, phone):
    key = name.capitalize()
    if len(key) == False or len(phone) == False:
        raise TypeError
    if not re.fullmatch(r"[a-zA-z]+", name):
        raise NameArgumentError
    if not re.fullmatch(r"[0-9]+", phone):
        raise PhoneArgumentError
    contacts[key] = phone
    return f"Contact {key}, with phone number {phone} successfully created"

@input_error
def change(name, phone):
    key = name.capitalize()
    if len(key) == False or len(phone) == False:
        raise TypeError
    if not re.fullmatch(r"[0-9]+", phone):
        raise PhoneArgumentError
    contacts[key] = phone
    return f"{key}'s phone number successfully changed on {phone}"

@input_error
def phone(name,*args,**kwargs):
    key = name.capitalize()
    return f"{key}'s phone is {contacts[key]}"


def show(*args, **kwargs):
    con ='\n'
    for i, j in contacts.items():
        con += ": ".join(["{:.>30}".format(i), "{:<20}".format(j)]) + "\n"
    return con


def bye(*args, **kwargs):
    sys.exit("Good bye!")


def info(*args,**kwargs):
    s = [
    "Commands should be entered with ONE whitespace between them and/or arguments, without quotes",
    "{:-^30}|{:-^35}|{:-^60}|".format("Command name", "Syntax", "Descrition"),
    "{:-^30}|{:-^35}|{:-^60}|".format("help", "help", "Show this page"),
    "{:-^30}|{:-^35}|{:-^60}|".format("hello", "hello", "Greetings"),
    "{:-^30}|{:-^35}|{:-^60}|".format("add", "add 'name' 'phone'", "Create a contact with 'name' and 'phone'"),
    "{:-^30}|{:-^35}|{:-^60}|".format("change", "change 'name' 'phone'", "Change a phone number 'phone' of the selected contact 'name'"),
    "{:-^30}|{:-^35}|{:-^60}|".format("phone", "phone 'name'", "Show a phone number of the selected contect 'name'"),
    "{:-^30}|{:-^35}|{:-^60}|".format("show all", "show all", "Show contact list"),
    "{:-^30}|{:-^35}|{:-^60}|".format("bye, close, exit, good bye", "any single word from the left list", "Exit this bot")
    ]
    return "\n".join(s)

commands = {
"hello": hello, 
"add": add, 
"change": change, 
"phone": phone, 
"show all": show, 
"good bye": bye,
"bye": bye,
"close": bye, 
"exit": bye,
"help": info
}

contacts = {
    "Vasyl": "380507777777"
}

if __name__ == "__main__":
    main()
