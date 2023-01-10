# private-collection

Web application to store and manage user collection of books

## **About the application**

App collects and stores information about user collection of books, its attributes and market values. User can add, delete and modify books he has in his list.

## **How it works**

To use the application it is required to be logged in. You can create and account by going to the registration page (Register), and then login (Login page). You can find all hyperlinks in navigation bar. When You are logged in You are on a home page with summarization of Your collection. You can use the navigation bar to go to the pages that shows all information about Your books (Books list), You can add books from existing sources (Add books) or create new custom book (New book).

## **Pages description - logging**

All pages used to manage user registration and logging to the application.

### **Login**

Here You can input credentials to login. When You input correct login and password You are directed to home page with information about Your collection.

### **Register**

When You don't have an account, You can create it here. The page checks if the login exists and if the password is strong enough. When everything is valid, and You click "Register" button You are being redirected to login page when You can input Your credentials.

### **Logout**

It's not rendering any pages, just removing user from response, so after this You will be logged out and loose the access to You collection.


## **Pages description - user interfaces**

Following pages are available only when user is logged in and shows information only about his collection.

### **Home**

Home page. If user has some books, then he can see the total cost of books and how much time will it take statistical Pole to read them all. Last element of the page is the button to remove all the users books (requires confirmation on popup window).

### **Books list**

If user have some books in his collection, here he can see the table with all the information about them. Also, You can edit or delete any book from the list with clicking one of the buttons next to the book.

### **Add books**

The page when You can add multiple books with using 2 methods. First is with the form that then will query api to get the books. Second method is to import the books from xls file. Using one of those methods redirects user to "Books list" page, where he can see updated list.

### **New book**

The page when You can add a book using the form. The form checks if the input is correct, and if it is then its adding the book to list.
