# UNIQUE web application (e-commerce NFT style)
UNIQUE is an e-commerce site that works with NFT style but with unique physical objects.
the app has two sections one for products that are posted by admin and this works as NFTs means that it only has a quantity of 1 and any customer who buys this item now is no longer in the market and it's in 
customer's inventory ready to resell it later with different price (greater than  or equals 1000$).
it also has a fans section that works as a link between customers in this section a customer could post a product that he 
owns physically not in the inventory and the details of the product and the customer himself would be displayed to other customers (something like olx)

- What does it do?  
 This is a web project that works as e-commerce.

- What "new features" have been implemented that we haven't seen before?  
 NFT style but with physical objects that are stored in physical inventory

## Prerequisites
- Python 
- Flask 
- Flask_Bcrypt
- Flask_Reuploaded
- flask_sqlalchemy
- flask_wtf  
- WTForms

## Features
- admins post products in the market section
- customers can request to add products in the fans section
- admins review customers' requests and accept or leave them in the pending section
- customer can log in and log out and sign up to the app
- admins can delete any item in the market or fans section
- customers are allowed to buy products from the market directly if their budget is enough
- every customer has a free 999 coins when he signs up
- customers can request to add more coins to their budget
- items' price must be greater than 1000 coin
- customers are allowed to view item details in both the fans and market section
- each customer has a profile page
- Anyone can view the profile pages of others

## Project Checklist
- [x] It is available on GitHub.
- [x] It uses the Flask web framework.
- [x] It uses at least one module from the Python Standard Library other than the random module.
- [x] It contains at least one class written by you that has both properties and methods. It uses `__init__()` to let the class initialize the object's attributes (note that  `__init__()` doesn't count as a method). This includes instantiating the class and using the methods in your app. Please provide below the file name and the line number(s) of at least one example of a class definition in your code as well as the names of two properties and two methods.
  - File name for the class definition: models.py
  - Line number(s) for the class definition: the whole file
  - Name of two methods: 6 
  - File name and line numbers where the methods are used: all over in route.py
- [x] It makes use of JavaScript in the front end and uses the localStorage of the web browser.
- [x] It uses modern JavaScript (for example, let and const rather than var).
- [x] It makes use of the reading and writing to the same file feature.
- [x] It contains conditional statements. Please provide below the file name and the line number(s) of at least
  one example of a conditional statement in your code.
  - File name: route.py
  - Line number(s): any POST route there is a condition inside the method 
- [x] It contains loops. Please provide below the file name and the line number(s) of at least
  one example of a loop in your code.
  - File name: route.px
  - Line number(s): in market route
- [x] It lets the user enter a value in a text box at some point.
  This value is received and processed by your back end Python code.
- [x] It doesn't generate any error message even if the user enters a wrong input.
- [x] It is styled using CSS.
- [x] The code follows the code and style conventions as introduced in the course, is fully documented using comments and doesn't contain unused or experimental code. 
  In particular, the code should not use `print()` or `console.log()` for any information the app user should see. Instead, all user feedback needs to be visible in the browser.  
- [x] All exercises have been completed as per the requirements and pushed to the respective GitHub repository.

## Run
- clone 
- install packages in Prerequisites 
- in the directory of the project itself run this command in cmd: `py run.py`

## Future work
- Enable customers to place orders for their physical items in inventory to be delivered to their homes.
- implement payment method to allow customers to add coins and add their cards
- in profile allow user image customized for each profile
- in profile page displays the user's inventory and previous purchases and the rate section
- allow users to have Auctions over items in the fans section (socket io)
  
## to test
- Admin: admin@gmail.com 
- customer1: assem@gmail.com 
- customer2: john@gmail.com
- customer: mohamed@gmail.com
- passwords for all users: 123456
