import sys
from PySide6 import QtCore, QtWidgets, QtGui
from pymongo import MongoClient
import pprint

class UiWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        try:
            self.dbcli = MongoClient()
            self.db = self.dbcli.python_todo.todo                            
        except Exception as error:
            print(error)
            print("could not connect to db")

        self.login_widgets = []
        self.username = None
        self.password = None
        self.text_username_input = QtWidgets.QLineEdit("username")        
        self.text_password_input = QtWidgets.QLineEdit("password")        
        self.button_confirm = QtWidgets.QPushButton("confirm")
        self.button_confirm.clicked.connect(self.make_login)                
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text_username_input)
        self.layout.addWidget(self.text_password_input)
        self.layout.addWidget(self.button_confirm)
        self.login_widgets.append(self.text_username_input)
        self.login_widgets.append(self.text_password_input)
        self.login_widgets.append(self.button_confirm)

        self.todos = []
        self.todo_widgets = []
        self.text = QtWidgets.QLabel("Your tasks",
                                     alignment=QtCore.Qt.AlignCenter)
        self.text_task_input = QtWidgets.QLineEdit("type task")
        self.button_add = QtWidgets.QPushButton("add")
        self.button_add.clicked.connect(self.add_task)
        self.todo_widgets.append(self.text_task_input)
        self.todo_widgets.append(self.button_add)
        self.todo_widgets.append(self.text)

    def add_task(self):
        print("task added")
        self.todos.append(self.text_task_input.text()+"\n") 
        s = ""
        for t in self.todos:
            print(t)
            s = s+str(t)
        self.text.setText(s)        
        try:
            filter = {"username": self.username, "password": self.password}
            new_val = {"$set": {"todos": self.todos}}
            self.db.update_one(filter, new_val)
        except:
            print("error adding to db")

    def make_login(self):
        self.username = self.text_username_input.text()
        self.password = self.text_password_input.text()
        print("making login with username ", self.username, " password ", self.password)
        for w in self.login_widgets:
            self.layout.removeWidget(w)      
            w.deleteLater()  
        found = False
        try:
            for doc in self.db.find():
                # pprint.pprint(doc)            
                if (doc["username"] == self.username and doc["password"] == self.password):
                    found = True
                    for item in doc["todos"]:
                        # print(item)
                        self.todos.append(item)
            if (found == False):
                dic = {}
                dic["username"] = self.username
                dic["password"] = self.password
                dic["todos"] = []
                self.db.insert_one(dic)
        except:
            print("Error ocurred loading todos")
        for w in self.todo_widgets:        
            self.layout.addWidget(w)            
        s = ""
        for t in self.todos:
            print(t)
            s = s+str(t)
            self.text.setText(s)
        self.layout.update()                

if __name__=="__main__":
    print("running")
    app = QtWidgets.QApplication([])

    ui = UiWidget()
    ui.show()

    sys.exit(app.exec())