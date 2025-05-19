from faker import Faker
import random

WIZ = Faker()

class BaseContact:
    def __init__(self, first_name, last_name, phone, email):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def contact(self):
        print(f"Wybieram numer {self.phone} i dzwonię do {self.first_name} {self.last_name}")

    @property
    def label_length(self):
        return len(f"{self.first_name} {self.last_name}")

class BusinessContact(BaseContact):
    def __init__(self, first_name, last_name, phone, email, position, company, business_phone):
        super().__init__(first_name, last_name, phone, email)
        self.position = position
        self.company = company
        self.business_phone = business_phone

    def contact(self):
        print(f"Wybieram numer {self.business_phone} i dzwonię do {self.first_name} {self.last_name}")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


def create_contacts(contact_type, number):
    contacts = []
    for _ in range(number):
        first_name = WIZ.first_name()
        last_name = WIZ.last_name()
        phone = WIZ.phone_number()
        email = WIZ.email()

        if contact_type == "base":
            contact = BaseContact(first_name, last_name, phone, email)
        elif contact_type == "business":
            position = WIZ.job()
            company = WIZ.company()
            business_phone = WIZ.phone_number()
            contact = BusinessContact(first_name, last_name, phone, email, position, company, business_phone)
        else:
            raise ValueError("Unknown contact type")

        contacts.append(contact)

    return contacts

KONTAKTY = create_contacts("business", 5)

print("\nWizytówki:")
for contact in KONTAKTY:
    print(str(contact))

print("\nSortowanie imienia:")
for contact in sorted(KONTAKTY, key=lambda c: c.first_name):
    print(contact)

print("\nSortowanie nazwiska:")
for contact in sorted(KONTAKTY, key=lambda c: c.last_name):
    print(contact)

print("\nSortowanie po e-mailu:")
for contact in sorted(KONTAKTY, key=lambda c: c.email):
    print(contact)

print("\nKontakt:")
KONTAKTY[0].contact()
print("Długość etykiety:", KONTAKTY[0].label_length - 1)