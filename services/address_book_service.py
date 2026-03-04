from datetime import date, datetime
from typing import final
from decorators.log_command_action import log_command_action
from models.contact import Contact
from models.contact_birthday import ContactBirthday
from models.table_row import TableData, TableRow
from services.base_service import BaseService
from utils.validator import Validator


@final
class AddressBookService(BaseService):
    """Сервіс для роботи з адресною книгою"""

    def find_contact_by_id(self, id: str) -> Contact | None:
        return next((contact for contact in self.contacts if contact.id == id), None)

    @log_command_action()
    def add_contact(self, data: dict) -> None:
        new_contact: Contact = Contact.from_dict(data)
        if not new_contact.is_valid():
            return
        self.contacts.append(new_contact)
        self.save()

    @log_command_action()
    def edit_contact(self, index: int, data: dict) -> None:
        updated_contact: Contact = Contact.from_dict(data)
        if not updated_contact.is_valid():
            return
        self.contacts[index] = updated_contact
        self.save()

    @log_command_action()
    def delete_contact(self, index: int) -> None:
        self.contacts.pop(index)
        self.save()

    def get_contacts_table_data(self, search_term: str) -> TableData:
        table_data: TableData = []
        for i, contact in enumerate(self.contacts):
            is_relevant: bool = any(
                contact_field_name != "id"
                and Validator.validate_search_term(contact_field_value, search_term)
                for contact_field_name, contact_field_value in contact.to_dict().items()
            )
            if not is_relevant:
                continue
            birthday_date: date | None = contact.birthday_date
            birthday: str = birthday_date.isoformat() if birthday_date else ""
            table_data.append(
                TableRow(
                    cells=[
                        contact.name,
                        contact.phone,
                        contact.email,
                        contact.address,
                        birthday,
                    ],
                    index=i,
                )
            )
        table_data.sort(key=lambda row: self._ukrainian_sort_key(row.cells[0]))
        return table_data

    def get_birthdays_table_data(self, days: int) -> TableData:
        table_data: TableData = []
        today: date = datetime.now().date()
        for i, contact in enumerate(self.contacts):
            birthday_date: date | None = contact.get_next_birthday_date(today)
            if not birthday_date or not self.is_birthday_soon(
                birthday_date, days, today
            ):
                continue
            table_data.append(
                TableRow(
                    cells=[
                        birthday_date.isoformat(),
                        contact.name,
                        contact.phone,
                        contact.email,
                        contact.address,
                    ],
                    index=i,
                )
            )
        table_data.sort(key=lambda row: row.cells[0])
        return table_data

    def get_dashboard_birthdays(self) -> list[str]:
        upcoming_contacts: list[ContactBirthday] = []
        for contact in self.contacts:
            next_birthday_date: date | None = contact.get_next_birthday_date()
            if next_birthday_date and self.is_birthday_soon(next_birthday_date, 7):
                upcoming_contacts.append(ContactBirthday(next_birthday_date, contact))
        upcoming_contacts.sort(key=lambda row: row.birthday_date)
        return (
            [
                f"  • {row.birthday_date.strftime('%d.%m')}: {row.contact.name}"
                for row in upcoming_contacts
            ]
            if upcoming_contacts
            else ["На найближчий тиждень іменинників немає"]
        )

    def is_birthday_soon(
        self,
        next_birthday_date: date,
        days: int,
        today: datetime | date = datetime.now().date(),
    ) -> bool:
        days_until: int = (next_birthday_date - today).days
        return 0 <= days_until <= days

    def save(self) -> None:
        self.storage.save([c.to_dict() for c in self.contacts])

    def reload(self) -> None:
        self.contacts = [Contact.from_dict(c) for c in self.storage.load_list()]
