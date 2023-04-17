Feature: Proﬁle management
    As a user, I want to be able to view and edit my proﬁle including my name, proﬁle picture, and bio.

    Scenario: Successful PNG Profile Picture Upload
        Given the first user is signed into their account
        When the first user is on the "Edit Profile" page
        And the first user chooses a PNG picture from their local storage
        And the first user enters the "Submit" button
        Then the first user will get a sucess message


    Scenario: Successful JPG Profile Picture Upload
        Given the second user is signed into their account
        When the second user is on the "Edit Profile" page
        And the second user chooses a JPG picture from their local storage
        And the second user enters the "Submit" button
        Then the second user will get a sucess message


    Scenario: Unsuccessful PDF Profile Upload
        Given the third user is signed into their account
        When the third user is on the "Edit Profile" page
        And the third user chooses a PDF file from their local storage
        And the third user enters the "Submit" button
        Then the third user will an error message