import shelve
from datetime import datetime
from website.models import Partners
partners_dict = {}
db_shelve = shelve.open('partner.db', 'c')
try:
    if 'PartnerInfo' in db_shelve:
        partners_dict = db_shelve['PartnerInfo']
    else:
        db_shelve['PartnerInfo'] = partners_dict
except:
    print("Error in retrieving Partner from database")
partner = Partners("ABC Bank", "Sembawang Road", "ABDBANK@gmail.com")
partners_dict[partner.get_id()] = partner
db_shelve['PartnerInfo'] = partners_dict
db_shelve.close()

partners = {}
db_shelve = shelve.open('partner.db', 'r')
try:
    partners = db_shelve['PartnerInfo']
    db_shelve.close()
except IOError:
    print("Error trying to read file")

except Exception as e:
    print(f"An unknown error has occurred,{e}")

partners_list = []
for key in partners:
    partner = partners.get(key)
    partners_list.append(partner)
print(partners_list)