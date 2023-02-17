# 1. User registration and login: Users should be able to create an account and log in to the app to access its features. (NS)
Feature: Microblog User Registration
    As a user, I want to be able to register an account on the Microblog application with a valid email and strong password.
    Scenario: Successful Registration [Partially Implemented]
        Given the user is on the Registration page
        When the user enters a unique username, a valid unused email, and a strong password
        And the user enters “register” button
        Then the user account is successfully created
        And the user is redirected to the login page
    Scenario: Non-Unique Username [Implemented]
        Given the user is on the Registration page
        When the user enters a non-unique username, a valid unused email, and a strong password
        And the user enters the “Register” button
        Then the user receives an error message
        And the user is prompted to enter a unique username
    Scenario: Invalid Email [Implemented]
        Given the user is on the Registration page
        When the user enters an invalid email, a unique username, and a strong password
        And the user enters “Register” button
        Then the user receives an error message
        And the user is prompted to enter a valid email
    Scenario: Weak Password [Not Implemented]
        Given the user is on the Registration page
        When the user enters a weak password, a unique username, a valid unused email
        And the user enters “Register” button
        Then the user receives an error message for the invalid input
        And the user is prompted to enter a stronger password
Feature: Microblog User Login
    As a user, I want to be able to log into and reset the password of my existing account on the Microblog application
    Scenario: Successful Login [Implemented]
        Given the user is on the Sign In page
        When the user enters a registered username and password
        And the user enters the “Sign In” button
        Then the user is successfully logged into their account
        And the user is redirected to the home page
    Scenario: Unregistered Username [Implemented]
        Given the user is on the Sign In page
        When the user enters an unregistered username address
        And the user enters the “Sign In” button
        Then the user receives an error message
    Scenario: Incorrect Password [Implemented]
        Given the user is on the Sign In page
        When the user enters an incorrect password
        And the user enters the “Sign In” button
        Then the user receives an error message
    Scenario: Forgotten Password [Partially Implemented]
        Given the user is on the Reset password page
        When the user enters the email address of a registered account
        And the user enters the “Request Password Reset” button
        Then the user is redirected to the Sign In page
        And the user receives an email to reset their password
    Scenario: Logout [Implemented]
        Given the user is on Microblog webpage
        And the user is logged in
        When the user clicks the Logout button on the navigation bar
        Then the user is logged out of their account
        And the user is redirected to the Sign In page
# 2. Proﬁle management: Users should be able to view and edit their proﬁles, including their name, proﬁle picture, and bio. (NS)
Feature: Proﬁle management
    As a user, I want to be able to view and edit my proﬁle including my name, proﬁle picture, and bio.
    Scenario: Successful Profile editing [Implemented]
        Given the user is signed into their account
        And the user is on the Profile page
        And the user clicks on the “Edit your profile” button
        When the user updates their profile with a new valid username and/or new bio
        And the user enters the “Submit” button
        Then the user can view the new profile updates
    Scenario: Successful Profile Picture Upload [Not Implemented]
        Given the user is on the signed into their account
        And the user is on the Profile page
        When the user clicks on the “Update Profile Picture” button
        And the user chooses a picture from their local storage
        And the user enters the “Submit” button
        Then the user will be able to view their new profile
    Scenario: Invalid Name [Implemented]
        Given the user is on the signed into their account
        And the user is on the Profile page
        And the user clicks on the “Edit your profile” button
        When the user updates their profile with an invalid/registered username
        And the user enters the “Submit” button
        Then the user receives an error message
        And the user is prompted to enter a username
# 3. Posting reviews: Users should be able to create and post reviews for diﬀerent items/products. (NB)
Feature: Posting Reviews
    As a user, I want to be able to create, edit, and delete reviews for different items/products.
    Scenario: A user successfully posts a review on the website. [Implemented]
        Given a user is signed into their account.
        And a user is on the home page.
        And a text-box field for the user to type a review.
        When the user inputs their review in the textbox
        And the user selects a Submit button.
        Then the review should appear on the section of the site.
        And the user is prompted a confirmation message
        And the site reflects the new changes
    Scenario: A user does not enter any text in the text field. [Implemented]
        Given a user is signed into their account.
        And a user is on the home page.
        And a text-box field for the user to type a review.
        When a user does not input any text into the textbox and clicks the “Submit” button.
        Then an error message is displayed
    Scenario: A user wants to edit a review they posted. [Not Implemented]
        Given a user is signed into their account.
        Given a user is on the subsection of the site where reviews are displayed.
        And an already published posts belongs to the user
        When a user presses an Edit button
        Then the text box is auto populated with the existing text from the previous review
        When a user replaces existing text with new text
        And presses the Submit button
        Then the review should appear on the section of the site
        And the user is prompted a confirmation message
        And the site reflects the new changes
    Scenario: A user wants to delete a review they posted. [Not Implemented]
        Given a user is signed into their account.
        And a user is on the subsection of the site where reviews are posted.
        And an already published review belongs to the user
        When A user presses an Delete button
        Then the review should be deleted from the section of the site
        And the user is prompted a confirmation message
        And the site reflects the new changes
# 4. Viewing reviews: Users should be able to view reviews posted by other users and ﬁlter them by product category. (NB)
Feature: Viewing Reviews
    As a user, I want to be able to view reviews posted by other users and filter them by product category.
    Scenario:  A user wants to view all posts. [Implemented]
        Given a user is signed into their account.
        When a user clicks on Explore button on the navigation bar
        Then the user is redirected to the Explore page with all reviews in chronological order
    Scenario:  A user wants to read reviews based on X category. [Not Implemented]
        Given a user is signed into their account.
        And a user is on the Explore page where reviews are posted by all users.
        When a user selects a filter by Category button
        And selects the desired X category from a picklist or dropdown
        Then the site refreshes
        And the page only contains reviews of products belonging to X category
    Scenario: A user wants to read reviews based on category, X, which does not exist on the site [Not Implemented]
        Given a user is signed into their account.
        And a user is on the Explore page where reviews are posted by all users.
        When a user selects a filter by Category button
        And does not find desired X category from a dropdown or picklist
        Then the site remains in its current state
        And the user selects another category option or exits the site
# 5. Commenting: Users should be able to add comments to reviews posted by other users. (AB)
Feature: Commenting
    As a user, I want to be able to look at comments made by other users on reviews as well as post my own.
    Scenario: A user wants to look at comments on a review [Implemented]
        Given the user is logged in
        And the user is on the Home or Explore page
        When the user clicks on a review they want to view
        Then comments on the review will appear, ordered by most recent
    Scenario: A user wants to comment on a review [Not Implemented]
        Given the user is logged in
        And the user is on the Home or Explore page
        And the user clicks on a review they want to view
        When the user enters text into the reply section
        And the user clicks the Submit button
        Then the user is prompted a confirmation message
        And the site reflects the new changes
# 6. Notiﬁcations: Users should receive notiﬁcations when someone comments on their reviews or when someone likes their reviews. (IA)
Feature: Notifications
    As a user, I want to receive notifications when someone interacts with my account such as, liking, or mentioning me in a post etc.
    Scenario: User receives a new notification successfully [Not Implemented]
        Given That the user has notifications on
        When The User’s post is liked, mentioned, or shared
        Then The user gets a notification
        And The user can see which post was liked, received a reply or user who followed him/her
        And The user can view the user who interacted with their account
    Scenario: User does not receive notification [Not Implemented]
        Given That the user disabled receiving notifications
        When a user is mentioned, gets a like or a reply on a post.
        And user is not notified
        Then the user can view the notification when the app is opened
        And users can see the replies, likes, and mentions.
# 7. Search: Users should be able to search for reviews and products by keywords. (IA)
Feature: Searching Engine [Partially Implemented]
    As a user, I want to search for information using keywords that are related to specific posts or users.
    Scenario: user successfully finds searched keyword
        Given That the user is logged in
        When The user writes a keyword in search box
        And Clicks Search
        Then search associated with keyword is displayed to the user
        And the user can scroll through the posts shown and user accounts associated with the keywords.
    Scenario: user cannot find searched keyword [Partially Implemented]
        Given a user is logged in
        When the user writes on the search box
        And clicks search
        Then The search bar does not return anything
        Then The searched keyword does not exist
        And the user views an empty page.
    Scenario: User Types wrong spelling [Partially Implemented]
        Given That the user is logged in
        When The user types the wrong spelling of the keyword
        And clicks search
        Then The search returns empty page
        And The user corrects the spelling
        Then The user receives keywords associated with the search.
        And The user can scroll through the posts shown and user accounts associated with the keywords.
# 8. User management: Admins should be able to manage user accounts, including the ability to block or delete accounts if necessary. (HQ)
Feature: As an admin, I should be able to block, activate, and delete accounts.
    Scenario: admin wants to delete a user account [Not Implemented]
        Given the user requested the account to be deleted
        When the user gives reason for account deletion
        And user proves ownership
        Then notify the user of account deletion
        And user approves of the deletion
        Then then the admin removes the user’s data and information from the system
        And the user cannot access the account or reactivate it after the given minimum.
    Scenario: Admin successfully reactivates user account [Not Implemented]
        Given The admin has access to Microblog system administration
        And That the user requested to reactivate their account
        When The user provides proof of ownership
        And The admin verifies the proof
        Then The admins click the activate button for the selected user
        And User receives email of account reactivation
        And The user is able to access their account and
    Scenario: admin wants to block a selected user account [Not Implemented]
        Given The user is reported by others or violates the community rights and guidelines
        When The admin reviews the report
        And The user violates the community rights and guidelines
        And Several warnings have been sent to the user
        When User continues to repeat the violations
        Then The admin blocks user from Microblog
        And The user cannot access their account until unblocked
    Scenario: Password reset
        Given that the user request to rest the password
        When  he user clicks on the forgot password button
        And  presses submit
        Then  then the user should get an email with a reset link
        And  the user can make a new password
# 9. Follow/Unfollow: Users should be able to follow and unfollow other users and see their reviews on a personalized timeline. (AA)
Feature: Follow and Unfollowing users
    As a user, I want to have the ability to follow and unfollow other users on the platform
    Scenario: Follow user [Implemented]
        Given a logged-in user
        When they click the follow button on a user
        Then they now follow that user
        And the follow button should change to say following
    Scenario: Unfollow a user [Implemented]
        Given a logged-in user
        When they click the following button on a user they follow
        Then a text box will pop up asking if they wish to unfollow that user
        And if the user clicks yes
        Then they unfollow that user
        And the following button should change to say follow
# 10. Like/dislike: Users should be able to like and dislike reviews and see the likes/dislikes count for each review. (AA)
Feature: Likes and Dislikes on reviews
    As a user, I want to able to see likes and dislikes, and like or dislike other reviews, and undo this as well
    Scenario: See other likes and dislikes [Not Implemented]
        Given a logged-in user
        When viewing a review (one's own or another users)
        Then there is an integer value displayed representing likes
        And another for dislikes
    Scenario: A user likes a post [Not Implemented]
        Given a logged-in user
        And the user clicks on a post
        When they click the like button
        Then the number of likes should increase by one
    Scenario: A user dislike a post [Not Implemented]
        Given a logged-in user
        And the user clicks on a post
        When they click the dislike button
        Then the number of dislikes should increase by one
# 11. Sharing: Users should be able to share reviews on social media platforms, such as Facebook, Twitter, and LinkedIn. (AA)
Feature: Sharing reviews
    As a user, I want to share reviews to Facebook, Twitter, LinkedIn, have the link to the review copied so I can use the link for other things, or export my posts
    Scenario: Share to Facebook [Not Implemented]
        Given a logged-in user
        When they click the share button
        Then options to share to Facebook, Twitter, LinkedIn, or copy link
        And they click Facebook
        Then they are redirected to Facebook to login and post a link to review
    Scenario: Share to Twitter [Not Implemented]
        Given a logged-in user
        When they click the share button
        Then options to share to Facebook, Twitter, LinkedIn, or copy link
        And they click Twitter
        Then they are redirected to Twitter to login and post a link to review
    Scenario: Share to LinkedIn [Not Implemented]
        Given a logged-in user
        When they click the share button
        Then options to share to Facebook, Twitter, LinkedIn, or copy link
        And they click LinkedIn
        Then they are redirected to LinkedIn to login and post a link to review
    Scenario: Copy Link [Not Implemented]
        Given a logged-in user
        When they click the share button
        Then options to share to Facebook, Twitter, LinkedIn, or copy link
        And they click copy link
        Then the link is put on their clipboard
    Scenario: Export Posts [Partially Implemented]
        Given a logged-in user
        And the user is on the profile page
        When they click the Export your Posts button
        Then the user will receive a downloadable copy of their post history
# 12. Bookmark: Users should be able to bookmark reviews and products, so they can easily ﬁnd them later. (HQ)
Feature: Bookmark
    As a user, I want to bookmark posts and weblinks to easily access them later.
    Scenario: A user successfully bookmarks a favourite article/post [Not Implemented]
        Given A user is registered on the site
        When the user sees a post and wants to bookmark it
        And the user presses on bookmark
        Then the post bookmarked is add to the bookmark section of the site
        And the user can view the post in the section
    Scenario: A user wants to remove a post from the bookmark section [Not Implemented]
        Given A user is logged in to the account
        Given A user has the post bookmarked
        When User opens the bookmark section
        And user is able to view all the bookmarked articles
        Then The user clicks on the “un-bookmark” button
        Then The site refreshes
        And User successfully removes the item from the section
    Scenario: A user successfully saves a post from the web [Not Implemented]
        Given A user is registered and logged in to the website
        When a user copies the URL of a weblink
        And the user pastes it to the Microblog bookmark URL search box
        Then The post is added to the bookmark section
        And The post is available for the user to view
# 13. User-generated tags: Users should be able to add tags to their reviews to make them more discoverable by other users. (AB)
Feature: User-generated tags
    As a user posting reviews, I want to be able to attach my own custom tags so other users can find my reviews more easily and my reviews will be shown alongside other relevant or similar reviews
    Scenario: A user wants to attach their tags when posting their review [Not Implemented]
        Given A logged in user with a written review not yet posted
        Then The system has another text box for the users to insert their custom tags, delimited by commas
        When The user clicks Post
        Then The system posts the review on the user’s profile with the generated tags
    Scenario: A user wants to add tags after they posted the review [Not Implemented]
        Given A logged in user and a review posted by said user
        When The user clicks Edit
        Then The system will open a page like the “create new review” page but with text areas populated with the previous input
        When The user enters their new tags in the text box, delimited by commas
        And Clicks Post
        Then The system updates the review with the newly generated tags
    Scenario: A user wants to look at more reviews with the same tag [Not Implemented]
        Given A logged in user
        When The user clicks on a user-generated tag, whether their own or on another review
        Then The system returns reviews that include the tag