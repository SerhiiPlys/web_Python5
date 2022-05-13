from abc import ABC, abstractmethod

class UserInterface(ABC):

    @abstractmethod
    def show_contact(self):
        pass

    @abstractmethod
    def show_note(self):
        pass

    @abstractmethod
    def show_help(self):
        pass

class ContactAdress():
    
    def __init__(self, adress = ''):
        self._adress = None
        self.adress = adress

    @property
    def adress(self):
        return self._adress

    @adress.setter
    def adress(self, adress):
        self._adress = adress

    def show_adress(self):
        print(self, end ='')

class ContactPhone():
    
    def __init__(self, phone = ''):
        self.__phone = None
        self.phone = phone

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone):
        self.__phone = phone

    def show_phone(self):
        print(self, end ='')

class ContactEmail():
    
    def __init__(self, email = ''):
        self.__email = None
        self.email = email

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    def show_email(self):
        print(self, end ='')


class ContactBirthday():
    
    def __init__(self, birthday = ''):
        self.__birthday = None
        self.birthday = birthday

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, birthday):
        self.__birthday = birthday

    def show_birthday(self):
        print(self, end ='')

# Классы похожи, но во всех них разная логика геттеров и сеттеров, а также еще не переопределен магический
# метод __str__ который для каждого класса будет отличаться 


class Contact(UserInterface):

    def __init__(self, name, adress:ContactAdress, phone:ContactPhone, email:ContactEmail, birthday:ContactBirthday) -> None:
        self.name = name
        self.adress = adress
        self.phone = phone
        self.email = email
        self.birthday = birthday


    def show_contact(self) -> None:
        print(self.name, end = '')  
        self.adress.show_adress()  
        self.phone.show_phone()  
        self.email.show_email()
        self.birthday.show_birthday()
        

class Note(UserInterface):

    def show_note(self, id) -> None:
        with open("note.txt", "r") as file:
            buffer = file.readlines()
        for item in buffer:
            if self.id == id:
                print (self)

class Help(UserInterface):

    def show_help(self) -> None:
        with open("help.txt", "r") as file:
            buffer = file.readlines()
        for item in buffer:
            print(item)

