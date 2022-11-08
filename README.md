# 1.3-and-1.4-Assessment - Libhub

## **About**
Welcome to Libhub. A library, borrowing/lending, website using Flask, SQlite using the ORM Flask-SQLalchemy, Flask-Login, Bootstrap 5, SCSS and Javascript. This assessment was made for the Level 1, 1.3 and 1.4, Digital Technologies Standards for NCEA. This project took approximately 20 hours to develop.

### My Purpose
My purpose for the assessment is to develop a place where my friends can borrow and lend books to each other, all in one place, using the website as a hub *(hence the name Libhub)* to track the process of borrowing and lending books. 

---

## **Prerequistes / How to run locally on cloning(downloading) repo**
1. Install a version of Python 3 (for which this tutorial is written). 

    - (Linux) The built-in Python 3 installation works well, but to install other Python packages you must run (bash/terminal)
        
            sudo apt install python3-pip 

2. Update pip:
        
        pip install --upgrade pip

3. Create a virtual env in VS Code

  
        python3 -m venv .venv (Mac/Linux)
  
        python -m venv .venv (Windows)


4. Accept the prompt to set this new enviornment as the new workplace settings. 

5. Install Python packages in *requirements.txt* using terminal:
        
        $ pip install -r requirements.txt

6. Install a version of [node.js](https://nodejs.org/en/download) (latest)

7. Run `npm ci` on terminal, which downloads the node_modules fodler

8. To run use `flask run`, and click the link provided to view.
   
---

## **How to run locally (for Moderation)**
1. Install a version of Python 3. 

    - (Linux) The built-in Python 3 installation works well, but to install other Python packages you must run (bash/terminal)
        
            sudo apt install python3-pip 

2. Update pip:
        
        pip install --upgrade pip


3. Install Python packages in *requirements.txt* using terminal:
        
        $ pip install -r requirements.txt

4. cd into the 1.3 and 1.4 assessment folder

4. To run use `flask run`, and click the link provided to view.
   
---


## **Libhub**
*My vision of Libhub is to provide end users (my friends) an easy, accessible and functional site to view, track, and lend books. In order to achieve that goal, I developed the website to be easy to use, accessible, functional, while maintaing visually pleasant aesthetics*

### **Overview**

---

### The Landing 

Upon entry, you will be greeted by the landing page. Which at a glance the navbar is easily visible at the top, this sticks to the top as we scroll down the page. The navbar, itself, contains links which helps the user to navigate around Libhub. The books link takes the user to *books page* where 4 of the most recently lended books are displayed. 

Additonally, here we can see the login links, that takes you to sign-up (if you don't have an account) or to log-in. **I created a authentication process (user accounts) for users to easily see who borrowed or lended what book.** 
The home page is aesthetic with minimal clutter and buttons, which act as links for different parts of Libhub, and a small descripton of the website. The colours I chose were high in contrast against the background *(All images are sourced from [Unsplash](https://unsplash.com/))*, which fit under the Web Content Accessibilty Guidelines (WCAG), a universal and international guidelines for websites across the web to ensure that all content is readable and accessible. This page will also changed, including the navbar, once the user has logged in.
<figure>
    <img src="assets /images/home.png" width="850px" height="475px">
    <em>
        <figcaption>The homepage of Libhub (not logged in)</figcaption>
    </em>
</figure>

As we scroll down the navbar still sticks at the top while giving it a solid black background. This is done to keep the navbar way from clipping to other texts as  it is originally transparent. The searchbar searches books based of the the book's title, its author, and the username of the user who lended the book. 
The cards visualises and represents Libhub's vision for a satisfactory end user experience.

- Borrow books at anytime
- Libhub's motto: 
    > *'If it exists we have it. If not start lending today'*
- Limitless control over your books

<figure>
    <img src="assets /images/home1.png" width="850px" height="475px">
    <em>
        <figcaption>Searchbar and cards for <em>aesthetics</em> and interactivity </figcaption>
    </em>
</figure>

The last part of the landing page includes the clickable carousel for testimonals *(albeit with fictonal characters)*, which was implemented to add a bit more flavour and flair to my website, as well as giving the end user a laugh, creating a sense of lightheartedness and ease as they navigate through the website. Making the overall user experience plesant to navigate and view through. 

Before the footer we have a section dedicated to explaining the lending and borrowing processes in Libhub. They also have buttons that takes you to the books page as well as the lend page (only accessible) once logged in. 

The footer, I believe, is the cherry on top. It adds a finshed look to the landing page while adding functionally. The links take you to the resepective pages, such as this Github page. While the privacy and Terms of Use links opens a seperate tab explaining the Terms and Conditons of Libhub. While this is unnecessary for website whose target audience is just my friends (interpersonal), it adds a bit of layering especailly when this project scales larger, adding more users (possibly user I don't know personally), the Privacy Policy and T&Cs declares the user's privacy rights for legal reasons. The footer is visble in most pages.

<figure>
    <img src="assets /images/home2.png" width="850px" height="475px">
    <em>
        <figcaption>Testimonals Carousel, more cards for <strong>aesthetics</strong> and footer</figcaption>
    </em>
</figure>

---

### The Library

The library page consists of the books that I personally haven't lended, here we can borrow books. 

<figure>
    <img src="assets /images/library.png" width="850px" height="475px">
    <em>
        <figcaption>The Library when logged in</figcaption>
    </em>
</figure>

When we scroll down we see the 4 most recent lended books by other users. Each card represents a book and it includes the book's title and its author as well. If we find a book that we like, we can request to borrow it by clicking the *borrow this book* link. If we aren't logged in we are taken to the login page. As users who are not logged in cannot borrow books.

<figure>
    <img src="assets /images/library2.png" width="850px" height="475px">
    <em>
        <figcaption>Books avaliable. Here we can borrow books</figcaption>
    </em>
</figure>

---

### Already have an account?

If the user tries access a page that has a login-requried attribute, which includes the borrowing, lending, as well as the personal dashboard pages, they will be redirected to the login page. Here, like any other login page, you can enter either the username associated to your account or the email and enter the password as well. If you don't have an account the link *Sign up now* will take you to the sign up page. 

<figure>
    <img src="assets /images/login.png" width="850px" height="475px">
    <em>
        <figcaption>Login page</figcaption>
    </em>
</figure>

Here is where you have to sign-up using a valid email while picking your username. Users will to confirm their password by making it sure it matches. The passwords must also be 7 characters long or more to ensure a strong password. Users who plugged in passwords that don't fit this criteria will be unable to create an account and a warning will pop up, forcing them to correct their mistake. Anothing is that users cannot share the same email or username, either one will lead to an warning to pop up. As long as there the criteria is met for sign up, the user will be created and be autonomically logged in. 

<figure>
    <img src="assets /images/sign-up.png" width="850px" height="475px">
    <em>
        <figcaption>Sign up page</figcaption>
    </em>
</figure>


<figure>
    <img src="assets /images/warning.png" width="1250px" height="42px">
    <em>
        <figcaption>Passwords do not match error</figcaption>
    </em>
</figure>

After sign up, the newly created user will be automatically redirected to the home page. Here a new version of the homepage can be seen. The first noticable difference is in the navbar. The sign up for free button turns into a logout button. A lend option is added to easily access the lend page. The user icon takes you to the account settings page, which allows the user to change their username, email, password, and other personal information. The dashboard, which allows the user to view books that've lended or borrowed, can be accessed by clicking the user's username. A pop up on hover will appear for users navigating. The sign up button on the main page turns a button to go to the books page. 

<figure>
    <img src="assets /images/home3.png" width="850px" height="475px">
    <em>
        <figcaption>The homepage of Libhub (logged in)</figcaption>
    </em>
</figure>


<figure>
    <img src="assets /images/popup.png" width="500px" height="200px">
    <em>
        <figcaption>Dashboard popup on hover</figcaption>
    </em>
</figure>

---

### Borrowing and Lending 

#### Lending

Lending at Libhub is easy. Click the lend button on the navbar (once logged in), or the the button at the front of the Books page. Here you have put the book's title and its author. There are special requriments in order to 

<figure>
    <img src="assets /images/lend.png" width="850px" height="475px">
    <em>
        <figcaption>Lending page</figcaption>
    </em>
</figure>

