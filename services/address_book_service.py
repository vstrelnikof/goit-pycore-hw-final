from datetime import date, datetime
from typing import final
from decorators.log_decorator import log_action
from models.contact import Contact
from models.contact_birthday import ContactBirthday
from services.base_service import BaseService

@final
class AddressBookService(BaseService):
    contacts: list[Contact]

    def find_contact_by_id(self, id: str) -> (Contact | None):
        return next((contact for contact in self.contacts if contact.id == id), None)

    @log_action
    def add_contact(self, data: dict) -> None:
        new_contact: Contact = Contact.from_dict(data)
        if not new_contact.is_valid():
            return
        self.contacts.append(new_contact)
        self.save()
    
    @log_action
    def edit_contact(self, index: int, data: dict) -> None:
        updated_contact: Contact = Contact.from_dict(data)
        if not updated_contact.is_valid():
            return
        self.contacts[index] = updated_contact
        self.save()

    @log_action
    def delete_contact(self, index: int) -> None:
        self.contacts.pop(index)
        self.save()
    
    def get_contacts_table_data(self, search_term: str) -> list[tuple[list[str], int]]:
        table_data: list[tuple[list[str], int]] = []
        for i, contact in enumerate(self.contacts):
            is_relevant: bool = any([contact for contact_field_name, contact_field_value
                                     in vars(contact).items()
                                     if contact_field_name != "id" and 
                                     search_term in contact_field_value.lower()])
            if not is_relevant:
                continue
            birthday_date: date | None = contact.birthday_date
            birthday: str = birthday_date.isoformat() if birthday_date else ""
            table_row: tuple[list[str], int] = ([contact.name,
                                                 contact.phone,
                                                 contact.email,
                                                 contact.address,
                                                 birthday], i)
            table_data.append(table_row)
        return table_data
    
    def get_birthdays_table_data(self, days: int) -> list[tuple[list[str], int]]:
        table_data: list[tuple[list[str], int]] = []
        today: date = datetime.now().date()
        for i, contact in enumerate(self.contacts):
            birthday_date: date | None = contact.get_next_birthday_date(today)
            if not birthday_date or not self.is_birthday_soon(birthday_date, days, today):
                continue
            table_row: tuple[list[str], int] = ([birthday_date.isoformat(),
                                                 contact.phone,
                                                 contact.email,
                                                 contact.address,
                                                 contact.name], i)
            table_data.append(table_row)
        table_data.sort(key=lambda table_row: table_row[0][0])
        return table_data

    def get_dashboard_birthdays(self) -> list[str]:
        upcoming_contacts: list[ContactBirthday] = []
        for contact in self.contacts:
            next_birthday_date: date | None = contact.get_next_birthday_date()
            if next_birthday_date and self.is_birthday_soon(next_birthday_date, 7):
                upcoming_contacts.append(ContactBirthday(next_birthday_date, contact))
        upcoming_contacts.sort(key=lambda row: row.birthday_date)
        return list(map(lambda row: f"  • {row.birthday_date.strftime('%d.%m')}: {row.contact.name}", upcoming_contacts)) \
            if upcoming_contacts else ["На найближчий тиждень іменинників немає"]
    
    def is_birthday_soon(self, next_birthday_date: date, days: int, today: datetime | date = datetime.now().date()) -> bool:
        days_until: int = (next_birthday_date - today).days
        return 0 <= days_until <= days

    def save(self) -> None:
        self.storage.save([c.to_dict() for c in self.contacts])

    def reload(self) -> None:
        self.contacts = [Contact.from_dict(c) for c in self.storage.load()]
