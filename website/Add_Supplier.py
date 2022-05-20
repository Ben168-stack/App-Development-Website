from website.models import Suppliers
import shelve

db_shelve = shelve.open('databases/supplier/supplier.db', 'c')
db_shelve_uniqueID = shelve.open('databases/supplier/supplier_uniqueID.db', 'c')
suppliers = {}
ids = 0
try:
    if "supplierinfo" in db_shelve:
        suppliers = db_shelve['supplierinfo']
    else:
        db_shelve['supplierinfo'] = suppliers
    if 'Id_info' in db_shelve_uniqueID:
        ids = db_shelve_uniqueID['Id_info']
    else:
        db_shelve_uniqueID['Id_info'] = ids

except IOError:
    print("Error trying to read file")

except Exception as e:
    print(f"An unknown error has occurred,{e}")

else:
    while True:
        choice = input("Create Supplier(1), Check Supplier database(2), Delete Supplier(3), Save Changes & Exit(4): ")
        if choice == '1':
            ids += 1
            name = input("Enter Supplier Name: ")
            supplier = Suppliers(name)
            supplier.set_id(ids)
            suppliers[ids] = supplier
            print("Suppliers database")
            for i in suppliers:
                print(f"{suppliers[i]}")


        elif choice == '2':
            for i in suppliers:
                print(f"{suppliers[i]}")
        elif choice == '3':
            print("Supplier Database:")
            for i in suppliers:
                print(f"{i}, {suppliers[i]}")
            try:
                choice = int(input("Enter an ID to delete"))
            except ValueError:
                print("Invalid Value")
            if choice in suppliers:
                del suppliers[choice]


        elif choice == '4':
            db_shelve['supplierinfo'] = suppliers
            db_shelve.close()
            db_shelve_uniqueID['Id_info'] = ids
            db_shelve_uniqueID.close()
            exit()

