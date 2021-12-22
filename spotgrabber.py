from selenium import webdriver
import time, random
import os
import getpass


# chromedriver paths
dirname = os.path.dirname(os.path.abspath(__file__))
browser = webdriver.Chrome(executable_path=dirname + "/chromedriver")


userName = ""
userPassword = ""

# flag to stop the script
spot_taken = False

possible_times = [
    "07:00-08:00",
    "08:00-09:00",
    "09:00-10:00",
    "10:00-11:00",
    "11:00-12:00",
    "12:00-13:00",
    "13:00-14:00",
    "14:00-15:00",
    "15:00-16:00",
    "16:00-17:00",
]
desired_times = []
desired_day = "do 23 dec 2021"


def main():
    user_input()
    print("Opening RSC website")
    browser.get("https://publiek.usc.ru.nl/publiek/login.php")

    login()

    expand_table()

    # try to fetch a spot
    while not spot_taken:
        print("Trying to fetch a spot...")
        fetch_and_take_spot()
        time.sleep(random.randint(30, 60))
        browser.refresh()
    print("Got a spot, script is done")


def user_input():
    user_satisfied = False
    while not user_satisfied:
        desired_times = []

        # get the day the user would like the train on
        print("Enter the day you would like to workout at as follows:")
        print("'wo 22 dec 2021' or 'di 7 jan 2022' or 'za 13 dec 2021'")
        input_val = input()
        desired_day = input_val
        cls()
        # Now get the times they would like
        print("Enter you desired timeslot options seperated by a comma")
        for i, t in enumerate(possible_times):
            print(str.format("Option {0}: {1}", i, t))
        input_val = input()
        choices = list(map(int, input_val.split(",")))
        # put times in the desired_times list
        for choice in choices:
            desired_times.append(possible_times[choice])

        cls()
        print(
            str.format(
                "The script will try to get a spot for "
                + "\033[1m"
                + "{0}"
                + "\033[0m"
                + " on the following times:",
                desired_day,
            )
        )
        print(desired_times)
        print("Type Y to continue and attempt to fetch a spot or N to try again")
        if input() != "Y":
            cls()
            continue
        else:
            user_satisfied = True

    print("Enter your RSC username")
    global userName
    userName = input()
    print("Enter your password")
    global userPassword
    userPassword = getpass.getpass()
    cls()


# to clear the terminal
def cls():
    os.system("cls" if os.name == "nt" else "clear")


def login():
    # get username and password field
    usernameField = browser.find_element_by_name("username")
    passwordField = browser.find_element_by_name("password")

    # send the username data
    usernameField.send_keys(userName)
    passwordField.send_keys(userPassword)

    # hit the submit button
    browser.find_element_by_xpath(
        "/html/body/div[3]/article/div[2]/div[2]/form/div[3]/div/button"
    ).click()


def expand_table():
    try:
        browser.get("https://publiek.usc.ru.nl/publiek/laanbod.php")
        time.sleep(1)

        browser.find_element_by_xpath(
            "/html/body/div[3]/article/article/form/label[1]/input"
        ).click()
    except:
        print("Something went wrong, maybe you entered a wrong password, idk")
        exit(0)


interesting_rows = []


def fetch_and_take_spot():
    interesting_rows = []
    time.sleep(1)
    table = browser.find_elements_by_xpath(
        "//*[@class= 'responstable clickabletr']/tbody/tr"
    )
    # Obtain the number of rows in body
    rows = 1 + len(table)

    # Printing the data of the table
    for r in range(2, rows):
        # obtaining the text from each column of the table
        value = browser.find_element_by_xpath(
            "//*[@class= 'responstable clickabletr']/tbody/tr["
            + str(r)
            + "]/td["
            + str(4)
            + "]"
        )
        if not value.text == "VOL ":
            timeV = browser.find_element_by_xpath(
                "//*[@class= 'responstable clickabletr']/tbody/tr["
                + str(r)
                + "]/td["
                + str(2)
                + "]"
            ).text
            day = browser.find_element_by_xpath(
                "//*[@class= 'responstable clickabletr']/tbody/tr["
                + str(r)
                + "]/td["
                + str(1)
                + "]"
            ).text
            # logic for deciding if we want it
            if day == desired_day and timeV in desired_times:
                take_spot(r)
                break


def take_spot(row_nr):
    # fetch the first spot of the interesting rows and register for it
    value = browser.find_element_by_xpath(
        "//*[@class= 'responstable clickabletr']/tbody/tr[" + str(row_nr) + "]"
    ).click()

    browser.find_element_by_xpath("/html/body/div[3]/article/div/div[1]/div/a ").click()
    browser.find_element_by_xpath("/html/body/div[3]/article/a[2]").click()
    browser.find_element_by_xpath(
        "/html/body/div[3]/article/div/form/fieldset/div/div[2]/div/button"
    ).click()
    global spot_taken
    spot_taken = True


if __name__ == "__main__":
    main()
