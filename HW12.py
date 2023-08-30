from collections import UserDict
from datetime import date
import re


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value) -> None:
        self._value = value

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other):
        if hasattr(other, "value"):
            value = other.value
        else:
            value = other
        return self.value == value


class Name(Field):
    pass


class Phone(Field):
    @staticmethod
    def phone_validation(phone: str) -> None:
        if not isinstance(phone, str):
            raise ValueError("Phone have to be str")
        if not phone.isdigit():
            raise ValueError("Phone have to include only digits")
        if 9 >= len(phone) <= 15:
            raise ValueError("Phone is too short or long")

    @Field.value.setter
    def value(self, phone: str) -> None:
        self.phone_validation(phone)
        Field.value.fset(self, phone)


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @staticmethod
    def birthday_validation(birthday: str) -> None:
        if type(birthday) != str: # isinstance
            raise ValueError("Phone have to be str")
        date_pattern = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(date_pattern, birthday):
            raise ValueError("Invalid birthday format. Please use 'YYYY-MM-DD' format.")

    @Field.value.setter
    def value(self, birthday: str) -> None:
        self.birthday_validation(birthday)
        Field.value.fset(self, birthday)


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = [phone] if phone is not None else []
        self.birthday = birthday

    def add_phone(self, phone: Phone):
        if phone in self.phones:
            raise ValueError(f"phone: {phone} is already in record")
        self.phones.append(phone)

    def delete_phone(self, phone: Phone):
        try:
            self.phones.remove(phone)
        except ValueError:
            raise ValueError(f"phone: {phone} not exists")

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        try:
            index = self.phones.index(old_phone)
            self.phones[index] = new_phone
        except ValueError:
            raise ValueError(f"old phone: {phone} not exists")

    def days_to_birthday(self):
        current_date = date.today()
        if self.birthday != None:
            birthday_date = date(self.birthday, "%Y-%m-%d")

            next_birthday_date = date(
                current_date.year, birthday_date.month, birthday_date.day
            )
            if current_date > next_birthday_date:
                next_birthday_date = date(
                    current_date.year + 1, birthday_date.month, birthday_date.day
                )

            return (next_birthday_date - current_date).days
        else:
            return f"This contact doesn't have the info about birthday"
        
    def __str__(self):
        str_phones = ", ".join(map(str, self.phones))
                
        return f'{self.name} {str_phones} {self.birthday}'
    
    def to_dict_record(self) -> dict[str, dict[str, list[str] | str | None]]:
        
        phones = []
        for phone in self.phones:
            phones.append(str(phone))

        if self.birthday is not None:
            birthday = str(self.birthday)
        else:
            birthday = None
        return {
            str(self.name): {
                "phones": phones,
                "birthday": birthday,
            }
        }



class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find_record(self, key_name: str):
        result = self.data.get(key_name)
        if self.data.get(key_name) == None:
            raise ValueError("There isn't such record")
        return result
    
    def __str__(self) -> str:
        return self.values

    def paginate(self, records_per_page: int):
        counter = 0
        list_rec = []
        for record in self.data.values():
            list_rec.append(record)
            counter += 1
            if not counter % records_per_page: 
                yield list_rec
                list_rec = []
            if counter == len(self.data):
                yield list_rec
    
    def find_contact(self, input_w: str):
        for record in self.data.values():
            str_val_record = f"{record.name} {' '.join([str(ph)for ph in record.phones])} {record.birthday}"
            if input_w.lower() in str_val_record.lower():
                yield record
    
    def to_dict_adrbook(self) -> dict:
        adr_book_dict = {}
        for record_j in self.data.values():
            adr_book_dict.update(record_j.to_dict_record())
        return adr_book_dict


if __name__ == "__main__":
    name_1 = Name("Bob_1")
    phone_1 = Phone("80123456789")
    b_day_1 = Birthday("1997-02-26")
    rec_1 = Record(name_1, phone_1, b_day_1)

    name_2 = Name("Bob_2")
    phone_2 = Phone("80123456789")
    b_day_2 = Birthday("2000-02-26")
    rec_2 = Record(name_2, phone_2, b_day_2)

    name_3 = Name("Anna")
    phone_3 = Phone("80123456789")
    b_day_3 = Birthday("1994-02-26")
    rec_3 = Record(name_3, phone_3, b_day_3)

    name_4 = Name("Oleg")
    phone_4 = Phone("80123456789")
    b_day_4 = Birthday("1997-02-26")
    rec_4 = Record(name_4, phone_4, b_day_4)

    name_5 = Name("Nico")
    phone_5 = Phone("80123456789")
    b_day_5 = Birthday("1999-02-26")
    rec_5 = Record(name_5, phone_5, b_day_5)

    phone_6 = Phone("80987654921")
    rec_5.add_phone(phone_6)
    ab = AddressBook()
    ab.add_record(rec_1)
    ab.add_record(rec_2)
    ab.add_record(rec_3)
    ab.add_record(rec_4)
    ab.add_record(rec_5)

    print(rec_1.to_dict_record())

    # for page in ab.paginate(2):
    #     input()
    #     a = " ".join(map(str, page))
    #     print(a, end="\n")

    for item in ab.find_contact("bo"):
        print(item)
    
    di = ab.to_dict_adrbook()
    print(di)

