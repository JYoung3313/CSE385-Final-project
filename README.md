# CSE385-Final-project
Final project for CSE385. a music database web application that allows users to discover, track, and rate songs and albums. The website will function similarly to Letterboxd, but instead of focusing on movies, it will focus on music. Users will be able to create accounts, search for music, submit ratings.


This project will include:


1. Database Design
First, we will design a relational database to store the information required for the application. Our database will include tables such as:
Users: Stores account information, including a unique user ID, username, email, and securely hashed password.
Artists: Stores information about musical artists.
Albums: Stores album information and references the associated artist.
Songs: Stores song information and references the album it belongs to.
Ratings: Stores user-submitted ratings, including the user, the song or album being rated, the rating value, and the submission date.
Listening History: Records which songs or albums a user has listened to and when they were logged.
We will establish primary and foreign keys to connect these tables and maintain referential integrity. For example, ratings will be associated with specific users and songs or albums, allowing us to retrieve a user's ratings or calculate the average rating for a particular piece of music.
2. Backend Development
Next, we will develop the backend using Python and the Flask framework. The backend will communicate with our MySQL database.
We will implement functionality for user registration and login, retrieving music information, recording listening history, and submitting or modifying ratings. We will also create SQL queries to calculate average ratings, retrieve top-rated music, and display users' previous activity.
Additionally, we will integrate the Discogs API to retrieve music information. When users search for an artist or album, the application will retrieve relevant information from the API and display the results. We will store selected music records in our own database so they can be associated with user ratings and listening histories.
3. Frontend Development
We will build the website's interface using HTML and CSS, along with JavaScript where necessary for interactive features.
The homepage will include a search bar, a random music discovery button, and a section displaying the highest-rated songs and albums. Individual music pages will display information about a selected song or album, its average user rating, and an option for logged-in users to submit their own ratings.
We will also create user profile pages where users can view their listening history and manage previously submitted ratings.
4. Testing and Finalization
After implementing the main features, we will test the application to ensure that the frontend, backend, database, and external API work together correctly.
Our testing will focus on verifying that users can successfully create accounts, search for music, submit ratings, and update or delete existing ratings. We will also check that average ratings are calculated correctly, listening histories are associated with the appropriate users, and the random music feature returns valid results.
Finally, we will address any identified issues, improve the website's usability, and prepare a demonstration showing the application's main features and database functionality.
Expected Outcome
By the end of the project, we aim to have a functional music-rating web application that demonstrates our understanding of relational database design, SQL queries, API integration, and full-stack web development. Users should be able to search for music, maintain a personal listening history, submit and manage ratings, and discover new songs and albums through community ratings and random recommendations.

5. User Manager Website Screenshots (5 pts)
Provide screenshots of the running User Manager website demo.
Note: You must connect to the school VPN to access the repository at CSE385A Database System Demo.
