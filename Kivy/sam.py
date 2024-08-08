from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivymd.app import MDApp

class ProfileCard(MDCard):
    pass

class EmployeeInfo(MDCard):
    employeeid = StringProperty("N/A")
    joined = StringProperty("N/A")
    designation = StringProperty("N/A")
    designationlevel = StringProperty("N/A")
    shift = StringProperty("N/A")

    def __init__(self, employeeid="N/A", joined="N/A", designation="N/A", designationlevel="N/A", shift="N/A", **kwargs):
        super().__init__(**kwargs)
        self.employeeid = employeeid
        self.joined = joined 
        self.designation = designation 
        self.designationlevel = designationlevel
        self.shift = shift 

class PersonalInfo(MDCard):
    firstname = StringProperty("N/A")
    lastname = StringProperty("N/A")
    fathername = StringProperty("N/A")
    mothername = StringProperty("N/A")
    address = StringProperty("N/A")
    phone = StringProperty("N/A")
    email = StringProperty("N/A")
    description = StringProperty("N/A")

    def __init__(self, firstname="N/A", lastname="N/A", mothername="N/A", fathername="N/A", address="N/A", email="N/A", phone="N/A", description="N/A", **kwargs):
        super().__init__(**kwargs)
        self.firstname = firstname 
        self.lastname = lastname
        self.mothername = mothername 
        self.fathername = fathername 
        self.address = address 
        self.phone = phone 
        self.email = email 
        self.description = description

Builder.load_file('sample.kv')

class SuccessScreen(BoxLayout):
    def __init__(self, **kw):
        super().__init__(**kw)

class MainApp(MDApp):
    employee_card = None
    personal_card = None

    def build(self):
        return SuccessScreen()

    def display_employeeinfo(self):
        self.root.ids.widget.text = "Employee Info"
        container = self.root.ids.scroll_container
        container.clear_widgets()
        
        if not self.employee_card:
            self.employee_card = EmployeeInfo(
                employeeid="12345",
                joined="2020-01-01",
                designation="Software Engineer",
                designationlevel="Level 2",
                shift="Morning",
                pos_hint={"center_x":.5,"center_y":.5},
				orientation='vertical'
            )
        
        container.add_widget(self.employee_card)

    def display_personalinfo(self):
        self.root.ids.widget.text = "Personal Info"
        container = self.root.ids.scroll_container
        container.clear_widgets()
        
        if not self.personal_card:
            self.personal_card = PersonalInfo(
                firstname="John",
                lastname="Doe",
                mothername="Jane Doe",
                fathername="James Doe",
                address="123 Main St",
                email="john.doe@example.com",
                phone="+1 234 567 890",
                description="A dedicated software engineer",
                pos_hint={"center_x":.5,"center_y":.5},
				orientation='vertical'
            )
        
        container.add_widget(self.personal_card)

if __name__ == "__main__":
    MainApp().run()
