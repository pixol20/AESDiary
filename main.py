from encryptor import encrypt
from encryptor import decrypt
import SaveLoad
from sys import exit
# variable that stores all encrypted entries
Entries = []

DiaryPassword = ""
# Check if file exists
if SaveLoad.CheckFile():
    DiaryPassword = input("Enter diary password: ")
    # try to decrypt file
    try:
        Entries = SaveLoad.LoadFile(DiaryPassword)
    except ValueError:
        print("Wrong password")
        exit(1)
else:
    # If it does not exist create a new password to save later
    DiaryPassword = input("Create a new password to encrypt diary file: ")
    Entries = []




def main():
    SaveLoad.SaveFile(Entries, DiaryPassword)
    print("AES Diary CLI")
    print("[0] Write a page")
    print("[1] Read a page")
    print("[2] Edit a page")
    print("[3] Change password")
    print("[4] Delete a page")
    print("[5] Display all entries")
    print("[6] Change diary encryption password")
    print("Anything else - Exit")
    print("Waiting for input: ", end="")
    UserInput = input()
    if UserInput == "0":
        WritePage()
    elif UserInput == "1":
        ReadPage()
    elif UserInput == "2":
        EditPage()
    elif UserInput == "3":
        ChangePassword()
    elif UserInput == "4":
        DeletePage()
    elif UserInput == "5":
        DisplayEntries()
    elif UserInput =="6":
        ChangeDiaryPassword()
    else:
        exit(0)


def WritePage():
    # Creates new dictionary called Page, encrypts data, saves into Page and appends it to entries
    Page = {}
    Title = input("Enter public title: ")
    UserInput = GetUserInput()
    password = input("enter password: ")
    Page = encrypt(UserInput, password, Title)
    Entries.append(Page)


def GetUserInput():
    print("Taking input, leave empty line to stop")
    lines = []

    while True:
        user_input = input()
        if user_input == '':
            break
        else:
            lines.append(user_input + '\n')

    return ''.join(lines)


def ReadPage():
    password = ""
    PageNum = 0
    EncryptedPage = {}

    # Check if integer
    try:
        PageNum = int(input("Enter page number: "))
    except ValueError:
        print("Please provide correct integer")
        ReadPage()
        return

    # Check if exists in Entries
    try:
        EncryptedPage = Entries[PageNum]
    except IndexError:
        print("Page does not exist")
        ReadPage()
        return

    password = input("Enter pasword: ")

    # Check if decrypts
    try:
        print(EncryptedPage["title"])
        print(decrypt(EncryptedPage, password).decode("utf-8"))
    except ValueError:
        print("Password is invalid")
        return


def EditPage():
    # Decrypts page, shows text that was on that page and takes input for a new one

    password = ""
    page = {}
    PageNum = 0
    text = ""
    # Check if integer
    try:
        PageNum = int(input("Enter page number: "))
    except ValueError:
        print("Please provide correct integer")
        EditPage()
        return

    # Check if exists in Entries
    try:
        page = Entries[PageNum]
    except IndexError:
        print("Page does not exist")
        EditPage()
        return

    password = input("Enter password: ")

    # Check if decrypts
    try:
        text = decrypt(page, password).decode('utf-8')
    except ValueError:
        print("Wrong password")
        EditPage()
        return


    print("Old text: ")
    print(text)
    print("New text: ")
    NewText = GetUserInput()
    Entries[Entries.index(page)] = encrypt(NewText, password, page['title'])


def ChangePassword():
    password = ""
    page = {}
    PageNum = 0
    text = ""

    # Check if integer

    try:
        PageNum = int(input("Enter page number: "))
    except ValueError:
        print("Please provide correct integer")
        ChangePassword()
        return

    # Check if exists in Entries
    try:
        page = Entries[PageNum]
    except IndexError:
        print("Page does not exist")
        ChangePassword()
        return

    password = input("Enter old password: ")

    # Check if decrypts
    try:
        text = decrypt(page, password).decode('utf-8')
    except ValueError:
        print("Wrong password")
        ChangePassword()
        return

    NewPassword = input("Enter new password: ")
    Entries[Entries.index(page)] = encrypt(text, NewPassword, page['title'])


def DeletePage():
    # Deletes page by index
    PageNum = 0
    # Check if integer
    try:
        PageNum = int(input("Enter page number: "))
    except ValueError:
        print("Please provide correct integer")
        DeletePage()
        return

    # Check if exists in Entries
    if PageNum > len(Entries) - 1:
        print("page does not exist")
        DeletePage()
        return

    Confirm = input("to confirm write y: ")
    if Confirm.upper() == "Y":
        Entries.pop(PageNum)
        print("Deleted")


def DisplayEntries():
    print()
    for i in range(len(Entries)):
        print(f"[{str(i)}] - {Entries[i]['title']}")
    print()

def ChangeDiaryPassword():
    # Changes global password used to encrypt
    global DiaryPassword
    DiaryPassword = input("Enter new password: ")


while True:
    main()