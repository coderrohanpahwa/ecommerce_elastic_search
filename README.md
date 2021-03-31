Multi Vendor Ecommerce Website 
Techonolgies used :
	Django (Backend)
	ElasticSearch (for autocompletion and fuzziness) and SQL for other purposes
	Frontend (HTML,CSS,JavaScript)
Prerequisites : 
 1. Make sure your elastic search client is running on local machine 
 2. Make sure to run pip requirements.txt (pip -r requirements.txt)
 3. Run all migrations (python manage.py migrate)  
 4. Add permission groups(seller and buyer) by running a script in a django shell ( python manage.py shell < adding_permissions.py)
 5. I have hardcoded shipment and location entries make sure you add an entry and run it 

Other things about the project : 
1. Fuziness and Autocompleyion is only handled for categories and name of product
2. If you have two vendors for selling a same product 2 entries are made in database being if vendor increases an amount of a particular product its get updated in Availability table 

Add your own frontend and feel free to use it anywhere.  
