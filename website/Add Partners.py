from website.models import Partners
import shelve

db_shelve = shelve.open('databases/partners/partners.db', 'c')
partners = {}
try:
    if "partnerinfo" in db_shelve:
        partners = db_shelve['partnerinfo']
    else:
        db_shelve['partnerinfo'] = partners
except IOError:
    print("Error trying to read file")

except Exception as e:
    print(f"An unknown error has occurred,{e}")

else:
    while True:
        choice = input("Create Partner(1), Check Partner database(2), Delete Partner(3), Save Changes & Exit(4): ")
        if choice == '1':
            name = input("Enter Partner's Company Name: ")
            location = input("Enter Partner's Company Location: ")
            partner = Partners(name,location)
            partners[partner.get_id()] = partner
            print("Partners database")
            for i in partners:
                print(f"{partners[i]}")


        elif choice == '2':
            for i in partners:
                print(f"{partners[i]}")
        elif choice == '3':
            print("Supplier Database:")
            for i in partners:
                print(f"{i}, {partners[i]}")
            try:
                choice = int(input("Enter an ID to delete"))
            except ValueError:
                print("Invalid Value")
            if choice in partners:
                del partners[choice]


        elif choice == '4':
            db_shelve['partnerinfo'] = partners
            db_shelve.close()
            exit()

