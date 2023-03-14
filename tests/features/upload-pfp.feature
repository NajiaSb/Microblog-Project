Feature: Proﬁle management
    As a user, I want to be able to view and edit my proﬁle including my name, proﬁle picture, and bio.

    Scenario: Successful Profile Picture Upload
        Given the user is signed into their account
        When the user is on the "Edit Profile" page
        And the user chooses a picture from their local storage
        And the user enters the "Submit" button
        Then the user will get a sucess message