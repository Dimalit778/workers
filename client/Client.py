import os, csv, json, requests
isOpen = True
message=""
srv_url = "http://srv:5000"

# FUNCTION TEST SERVER
def testServer():
    res = requests.get(srv_url + "/test")
    print(res.text)

#------- FUNCTION ADD WORKER  ---------
def addWorker():
    #GET WORKER DETAILS FROM USER INPUT
    try:
        print("Please insert first name, last name, age, id, email")
        userInput = input()
        userInput = userInput.split(',')
        newWorker = {
            "firstname": userInput[0],
            "lastname": userInput[1],
            "age": int(userInput[2]),
            "id": userInput[3],
            "email": userInput[4]
        }
    except:
        print("Invalid input")
    # SEND A POST REQUEST TO SERVER
    res = requests.post(srv_url + "/addworker", json=newWorker)

    print(res.text)

# ----- FUNCTION REMOVE WORKER -------
def removeWorker():
    # GET WORKER ID
    try:
        print("Please insert worker id to remove")
        userInput = input()
        removeId = {
            "id": userInput,
        }
    except:
        print("Invalid input")
        # SEND A DELETE REQUEST TO SERVER
    res = requests.delete(srv_url + "/removeworker", json=removeId)
    print(res.text)


# ------ FUNCTION UPDATE WORKER -----
def updateWorker():
    # GET WORKER BY ID
    try:
        print("Please insert worker id to update")
        toUpdate = input()
        idToUpdate = {
            "id": toUpdate,
        }
    except:
           print("Invalid input")
    res = requests.get(srv_url + "/worker", json=idToUpdate)  # SEND A GET REQUEST TO SERVER
    openUpdate = True   # CREATE BOOLEAN CONDISION
    # GET WORKER DETAILS TO DATA
    data = res.text.replace("[","").replace("]","").replace(",","").replace('"','').split()

    # STORE DATA INFO TO NEW WORKER
    updateWorkerDetails = {
       "firstname": data[1],
       "lastname": data[2],
       "age": int(data[3]),
       "id": data[4],
       "email": data[5],
       "workerid": int(data[0])
    }
    # SHOW MANU TO UPDATE EVERY DETAIL OF WORKER
    while(openUpdate):
        print(updateWorkerDetails)  # SHOW WORKER INFO
        showMenuUpdate()     # SHOW UPDATE MENU
        userChoice = int(input())   # GET USER CHOSIE

        if(userChoice==5):   # IF USER CHOISE 5 IT WILL END THE UPDATE
            openUpdate=False
        else:
            # UPDATE WORKER INFO
            functionUpdateCalls[userChoice](updateWorkerDetails)


    global message   # MESSAGE
    message = updateWorkerDetails   # STORE UPDATE WORKER IN MESSAGE
    # SEND A PUT REQUEST TO SERVER
    res = requests.put(srv_url + "/updateworker", json=updateWorkerDetails)
    print(res.text)

# ----- FUNCTION SHOW ALL WORKERS ------
def showAllWorkers():
    res = requests.get(srv_url + "/allworkers")  # SEND A GET REQUEST TO SERVER
    global message
    message = res.text  # STORE RES IN MESSAGE
    print(res.text)

# ----- FUNCTION IMPORT CSV -----
def importCsv():
    fieldnames = ['workerid', 'firstname', 'lastname', 'age', 'id', 'email']
    file = open('workers.csv', 'w', encoding='UTF8', newline='')

    csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
    csv_writer.writeheader()
    res = requests.get(srv_url + "/allworkers")
    data = res.json()
    result = list()
    for w in data:
         user= {
         'workerid': w[0],
         'firstname': w[1],
         'lastname': w[2],
         'age': w[3],
         'id': w[4],
         'email': w[5]
         }
         result.append(user)
    csv_writer.writerows(result)
    file.close

# FUNCTION EXPORT CSV
def exportCsv():
    file = open('workers.csv' ,'r', encoding='UTF8')
    global message
    message = file.read()
    file.close

# ALL FUNCTIONS OF UPDATE WORKER
def exit():
    global isOpen
    isOpen = False

def editFirstName(worker):
    print("Please insert worker first name")
    worker['firstname'] = input()

def editLastName(worker):
    print("Please insert worker last name")
    worker['lastname'] = input()

def editAge(worker):
    print("Please insert worker age")
    worker['age'] = int(input())

def editId(worker):
    print("Please insert worker id")
    worker['id'] = input()

def editEmail(worker):
    print("Please insert worker email")
    worker['email'] = input()

# CALL THE UPDATE FUNCTIONS
functionUpdateCalls = {
    0: editFirstName,
    1: editLastName,
    2: editAge,
    3: editId,
    4: editEmail
}

# MANU TO UPDATE WORKER
def showMenuUpdate():
    print("Choose what you want to update:")
    print("0. First name")
    print("1. Last name ")
    print("2. Age")
    print("3. Id")
    print("4. Email")
    print("5. Finish Update")

# MANU FUNCTIONS
functionCalls = {
    0: testServer,
    1: addWorker,
    2: removeWorker,
    3: updateWorker,
    4: showAllWorkers,
    5: importCsv,
    6: exportCsv,
    7: exit
}

# MAIN MANU
def showMenu():
    print("Please choose:")
    print("0. Test server")
    print("1. Add worker")
    print("2. Remove worker")
    print("3. Update worker")
    print("4. Show all workers")
    print("5. Import workers list from CSV")
    print("6. Export workers list to CSV")
    print("7. Exit")
    #PRINT MESSAGE
    global message
    print(message)

def main():
    print("Welcome to workers system:")
    while(isOpen):
        # SHOW MANU
        showMenu()
        # CHOOSE FROM MANU
        userChoice = int(input())
        # CALL FUNCTION
        functionCalls[userChoice]()
        # CLEAR TERMINAL
        os.system("clear")
    print("Bye Bye, have a nice day!")

if __name__ == "__main__":
    main()


