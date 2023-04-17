Feature: Microblog Multi Factor Authentication
    As a user, I want to be able to log into my account securly using a MFA token on my phone

    Scenario: Successful Login
        Given the first mfa user is on the login page
        When the first mfa user enters user1 in the username field
        And the first mfa user enters Password1@ in the password field
        And the first mfa user enters 111111 in the token field
        And the first mfa user clicks the "Sign in" button
        Then the first mfa user is redirected to the home page

    Scenario: Unsuccessful Login
        Given the second mfa user is on the login page
        When the second mfa user enters user1 in the username field
        And the second mfa user enters Password1@ in the password field
        And the second mfa user enters 123456 in the token field
        And the second mfa user clicks the "Sign in" button
        Then the second mfa user gets an error message

    Scenario: Short MFA Token Login
        Given the third mfa user is on the login page
        When the third mfa user enters user1 in the username field
        And the third mfa user enters Password1@ in the password field
        And the third mfa user enters 12345 in the token field
        And the third mfa user clicks the "Sign in" button
        Then the third mfa user gets an error message

    Scenario: Long MFA Token Login
        Given the fourth mfa user is on the login page
        When the fourth mfa user enters user1 in the username field
        And the fourth mfa user enters Password1@ in the password field
        And the fourth mfa user enters 1234567 in the token field
        And the fourth mfa user clicks the "Sign in" button
        Then the fourth mfa user gets an error message