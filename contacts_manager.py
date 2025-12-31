"""
Contact Management System
Week 3: Functions & Dictionaries Project
A comprehensive contact manager with CRUD operations, validation, and persistence.
"""

import json
import re
import csv
import os
from datetime import datetime, timedelta


# ==================== VALIDATION FUNCTIONS ====================
def validate_phone(phone):
    """Validate phone number format (10-15 digits)"""
    digits = re.sub(r'\D', '', phone)
    return (True, digits) if 10 <= len(digits) <= 15 else (False, None)


def validate_email(email):
    """Validate email format (optional field)"""
    if not email:
        return True
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


# ==================== FILE OPERATIONS ====================
def load_contacts(filename="contacts_data.json"):
    """Load contacts from JSON file"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                contacts = json.load(file)
                print("✅ Contacts loaded successfully!")
                return contacts
        else:
            print("📂 No existing contacts file found. Starting fresh.")
            return {}
    except (json.JSONDecodeError, IOError) as e:
        print(f"⚠️ Error loading contacts: {e}. Starting fresh.")
        return {}


def save_contacts(contacts, filename="contacts_data.json"):
    """Save contacts to JSON file"""
    try:
        with open(filename, 'w') as file:
            json.dump(contacts, file, indent=2)
        return True
    except IOError as e:
        print(f"❌ Error saving contacts: {e}")
        return False


# ==================== CRUD FUNCTIONS ====================
def add_contact(contacts):
    """Add a new contact with validation"""
    print("\n" + "="*50)
    print("ADD NEW CONTACT")
    print("="*50)
    
    # Get name
    while True:
        name = input("Enter contact name: ").strip()
        if name:
            if name in contacts:
                print(f"⚠️ '{name}' already exists!")
                choice = input("Update instead? (y/n): ").lower()
                if choice == 'y':
                    update_contact(contacts, name)
                    return contacts
                else:
                    continue
            break
        print("❌ Name cannot be empty!")
    
    # Get phone with validation
    while True:
        phone = input("Enter phone number: ").strip()
        is_valid, cleaned = validate_phone(phone)
        if is_valid:
            break
        print("❌ Invalid! Enter 10-15 digits (e.g., 1234567890)")
    
    # Get email with validation
    while True:
        email = input("Email (press Enter to skip): ").strip()
        if not email or validate_email(email):
            break
        print("❌ Invalid email format!")
    
    # Additional info
    address = input("Address (optional): ").strip()
    group = input("Group (Friends/Work/Family/Other): ").strip().title() or "Other"
    
    # Store contact
    contacts[name] = {
        'phone': cleaned,
        'email': email if email else None,
        'address': address if address else None,
        'group': group if group in ['Friends', 'Work', 'Family'] else 'Other',
        'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    print(f"✅ '{name}' added successfully!")
    return contacts


def search_contacts(contacts, search_term):
    """Search contacts by name (case-insensitive partial match)"""
    search_term = search_term.lower()
    results = {}
    
    for name, info in contacts.items():
        if search_term in name.lower():
            results[name] = info
    
    return results


def display_search_results(results):
    """Display search results in formatted way"""
    if not results:
        print("📭 No contacts found.")
        return
    
    print(f"\n📋 Found {len(results)} contact(s):")
    print("-" * 50)
    
    for i, (name, info) in enumerate(results.items(), 1):
        print(f"{i}. 👤 {name}")
        print(f"   📞 Phone: {format_phone(info['phone'])}")
        if info['email']:
            print(f"   📧 Email: {info['email']}")
        if info['address']:
            print(f"   📍 Address: {info['address']}")
        print(f"   👥 Group: {info['group']}")
        print(f"   📅 Updated: {info['updated']}")
        print()


def update_contact(contacts, name=None):
    """Update existing contact information"""
    if not name:
        print("\n" + "="*50)
        print("UPDATE CONTACT")
        print("="*50)
        name = input("Enter contact name to update: ").strip()
    
    if name not in contacts:
        print(f"❌ Contact '{name}' not found!")
        return contacts
    
    print(f"\nUpdating contact: {name}")
    print("Leave fields blank to keep current values.")
    print("-" * 30)
    
    # Current info
    current = contacts[name]
    print(f"Current phone: {format_phone(current['phone'])}")
    
    # Update phone
    while True:
        new_phone = input(f"New phone [{format_phone(current['phone'])}]: ").strip()
        if not new_phone:
            break
        is_valid, cleaned = validate_phone(new_phone)
        if is_valid:
            current['phone'] = cleaned
            break
        print("❌ Invalid phone number!")
    
    # Update email
    while True:
        current_email = current['email'] or ''
        new_email = input(f"New email [{current_email}]: ").strip()
        if not new_email:
            break
        if validate_email(new_email):
            current['email'] = new_email if new_email else None
            break
        print("❌ Invalid email format!")
    
    # Update other fields
    current_address = current['address'] or ''
    new_address = input(f"New address [{current_address}]: ").strip()
    if new_address:
        current['address'] = new_address
    
    current_group = current['group']
    new_group = input(f"New group [{current_group}]: ").strip().title()
    if new_group and new_group in ['Friends', 'Work', 'Family', 'Other']:
        current['group'] = new_group
    
    # Update timestamp
    current['updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"✅ '{name}' updated successfully!")
    return contacts


def delete_contact(contacts):
    """Delete a contact with confirmation"""
    print("\n" + "="*50)
    print("DELETE CONTACT")
    print("="*50)
    
    name = input("Enter contact name to delete: ").strip()
    
    if name not in contacts:
        print(f"❌ Contact '{name}' not found!")
        return contacts
    
    # Show contact info
    info = contacts[name]
    print(f"\nContact to delete:")
    print(f"Name: {name}")
    print(f"Phone: {format_phone(info['phone'])}")
    if info['email']:
        print(f"Email: {info['email']}")
    print(f"Group: {info['group']}")
    
    # Confirm deletion
    confirm = input(f"\n⚠️ Are you sure you want to delete '{name}'? (y/n): ").lower()
    if confirm == 'y':
        del contacts[name]
        print(f"✅ '{name}' deleted successfully!")
    else:
        print("❌ Deletion cancelled.")
    
    return contacts


def display_all_contacts(contacts):
    """Display all contacts in formatted way"""
    if not contacts:
        print("\n📭 No contacts in your address book.")
        return
    
    print(f"\n" + "="*50)
    print(f"ALL CONTACTS ({len(contacts)} total)")
    print("="*50)
    
    for i, (name, info) in enumerate(contacts.items(), 1):
        print(f"{i}. 👤 {name}")
        print(f"   📞 {format_phone(info['phone'])}")
        print(f"   👥 {info['group']}")
        print(f"   📅 Last updated: {info['updated']}")
        print()


# ==================== UTILITY FUNCTIONS ====================
def format_phone(phone):
    """Format phone number for display"""
    if len(phone) == 10:
        return f"({phone[:3]}) {phone[3:6]}-{phone[6:]}"
    elif len(phone) == 11:
        return f"+{phone[0]} ({phone[1:4]}) {phone[4:7]}-{phone[7:]}"
    return phone


def export_to_csv(contacts):
    """Export contacts to CSV file"""
    if not contacts:
        print("❌ No contacts to export!")
        return
    
    filename = f"contacts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Phone', 'Email', 'Address', 'Group', 'Created', 'Updated'])
            
            for name, info in contacts.items():
                writer.writerow([
                    name,
                    format_phone(info['phone']),
                    info['email'] or '',
                    info['address'] or '',
                    info['group'],
                    info['created'],
                    info['updated']
                ])
        
        print(f"✅ Contacts exported to '{filename}'")
    except IOError as e:
        print(f"❌ Error exporting to CSV: {e}")


def show_statistics(contacts):
    """Display contact statistics"""
    if not contacts:
        print("\n📭 No contacts to show statistics for.")
        return
    
    print("\n" + "="*50)
    print("CONTACT STATISTICS")
    print("="*50)
    
    total = len(contacts)
    print(f"📊 Total Contacts: {total}")
    
    # Group statistics
    groups = {}
    for info in contacts.values():
        group = info['group']
        groups[group] = groups.get(group, 0) + 1
    
    print("\n📈 Contacts by Group:")
    for group, count in sorted(groups.items()):
        print(f"  • {group}: {count} contact(s)")
    
    # Recently updated (last 7 days)
    recent_count = 0
    week_ago = datetime.now() - timedelta(days=7)
    
    for info in contacts.values():
        updated = datetime.strptime(info['updated'], "%Y-%m-%d %H:%M:%S")
        if updated > week_ago:
            recent_count += 1
    
    print(f"\n🔄 Recently Updated (last 7 days): {recent_count}")


# ==================== MAIN MENU ====================
def display_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("CONTACT MANAGEMENT SYSTEM")
    print("="*50)
    print("1. 📝 Add New Contact")
    print("2. 🔍 Search Contact")
    print("3. ✏️ Update Contact")
    print("4. 🗑️ Delete Contact")
    print("5. 📋 View All Contacts")
    print("6. 📤 Export to CSV")
    print("7. 📊 View Statistics")
    print("8. 💾 Save & Exit")
    print("="*50)


def main():
    """Main program function"""
    print("\n" + "="*50)
    print("🚀 WELCOME TO CONTACT MANAGEMENT SYSTEM")
    print("="*50)
    
    # Load existing contacts
    contacts = load_contacts()
    
    while True:
        display_menu()
        
        try:
            choice = input("Enter your choice (1-8): ").strip()
            
            if choice == '1':
                contacts = add_contact(contacts)
                save_contacts(contacts)
                
            elif choice == '2':
                print("\n" + "="*50)
                print("SEARCH CONTACTS")
                print("="*50)
                search_term = input("Enter name to search: ").strip()
                results = search_contacts(contacts, search_term)
                display_search_results(results)
                
            elif choice == '3':
                contacts = update_contact(contacts)
                save_contacts(contacts)
                
            elif choice == '4':
                contacts = delete_contact(contacts)
                save_contacts(contacts)
                
            elif choice == '5':
                display_all_contacts(contacts)
                
            elif choice == '6':
                export_to_csv(contacts)
                
            elif choice == '7':
                show_statistics(contacts)
                
            elif choice == '8':
                if save_contacts(contacts):
                    print("\n✅ Contacts saved successfully!")
                print("\n" + "="*50)
                print("Thank you for using Contact Management System!")
                print("="*50)
                break
                
            else:
                print("❌ Invalid choice! Please enter 1-8.")
                
        except KeyboardInterrupt:
            print("\n\n⚠️ Program interrupted. Saving contacts...")
            save_contacts(contacts)
            print("Goodbye!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    main()