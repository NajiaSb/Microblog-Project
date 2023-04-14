Feature: Microblog User Registration
    As a user, I want to be able to register an account on the Microblog application with a valid email and strong password
    that consists of minimum 8 characters with at least 1 capital letter, 1 number, and 1 special character.

    Scenario: Successful Registration
        Given the first user is on the Registration page
        When the first user enters "test1" in the username field
        And the first user enters "test1@example.com" in the email field
        And the first user enters "Password1@" in the password field
        And the first user enters "Password1@" in the repeat password field
        And the first user clicks the "Submit" button
        Then the first user is redirected to mfa page

    Scenario: Unsuccessful Registration with Missing Capital Letter
        Given the second user is on the Registration page
        When the second user enters "test2" in the username field
        And the second user enters "test2@example.com" in the email field
        And the second user enters "password1@" in the password field
        And the second user enters "password1@" in the repeat password field
        And the second user clicks the "Submit" button
        Then the second user will get a message error stating criteria of password

    Scenario: Unsuccessful Registration with Missing Number
        Given the third user is on the Registration page
        When the third user enters "test3" in the username field
        And the third user enters "test3@example.com" in the email field
        And the third user enters "Password@" in the password field
        And the third user enters "Password@" in the repeat password field
        And the third user clicks the "Submit" button
        Then the third user will get a message error stating criteria of password

    Scenario: Unsuccessful Registration with Missing Special Character
        Given the fourth user is on the Registration page
        When the fourth user enters "test4" in the username field
        And the fourth user enters "test4@example.com" in the email field
        And the fourth user enters "Password1" in the password field
        And the fourth user enters "Password1" in the repeat password field
        And the fourth user clicks the "Submit" button
        Then the fourth user will get a message error stating criteria of password

    Scenario: Unsuccessful Registration with Password Less than 8 Characters
        Given the fifth user is on the Registration page
        When the fifth user enters "test5" in the username field
        And the fifth user enters "test5@example.com" in the email field
        And the fifth user enters "Psw@1" in the password field
        And the fifth user enters "Psw@1" in the repeat password field
        And the fifth user clicks the "Submit" button
        Then the fifth user will get a message error stating criteria of password