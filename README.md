# Dating App

This is a dating application that allows users to register, view profiles of other users, update their location, and connect with other users by expressing mutual interest.

The project uses environment variables, and here is an example of the file: example.env

## API Endpoints

### User Registration [/api/clients/create/]

- Method: `POST`
- Request Type: `form-data`
- Request Body:
    - `avatar` (image file): User profile photo.
    - `gender` (string): User's gender ('M' for male or 'F' for female).
    - `first_name` (string): User's first name.
    - `last_name` (string): User's last name.
    - `email` (string): User's email address.
    - `longitude` (FloatField): User's current longitude (optional field).
    - `latitude` (FloatField): User's current latitude (optional field).
- Response:
    - Status Code: 201 - Created

The image is processed, and a watermark is applied to it (sample).

### Adding a User to the Match List [/api/clients/{id}/match/]

- Method: `POST`
- Permissions: Authenticated User
- URL Parameters:
    - `id` (integer): The identifier of the user to be added to the match list.
- Request Body: Not applicable
- Response:
    - Status Code: 200 - OK
    - Body:
        - `message` (string): A message indicating successful addition of the user to the match list.
  
If the interest is mutual, an email is sent to both participants.

### Get List of Participants [/api/list/]

- Method: `GET`
- Permissions: Authenticated User
- Request Parameters:
    - `gender` (string, optional): Filter participants by gender.
    - `first_name` (string, optional): Filter participants by first name.
    - `last_name` (string, optional): Filter participants by last name.
    - `distance` (string, optional): Display participants within a certain radius from the user in kilometers.
Example Request: /api/list/?gender=M&distance=200 - display males within a 200 km radius.  

- Response:
    - Status Code: 200 - OK
    - Body: An array of participant objects, each containing the following fields:
        - `id` (integer): Participant's identifier.
        - `avatar` (string): URL of the participant's avatar.
        - `gender` (string): Participant's gender.
        - `first_name` (string): Participant's first name.
        - `last_name` (string): Participant's last name.
        - `email` (string): Participant's email address.
        - `longitude` (float): Longitude coordinates of the participant's current location.
        - `latitude` (float): Latitude coordinates of the participant's current location.

### Update User Data [/api/clients/update/]

- Method: `PUT`
- Permissions: Authenticated User
- Request Body may include:
    - `first_name` (image file): New first name.
    - `last_name` (string): New last name.
    - `avatar` (image file): New avatar.
    - `password` (string): New password.
    - `longitude` (float): New longitude coordinates of the user's location.
    - `latitude` (float): New latitude coordinates of the user's location.
- Response:
    - Status Code: 200 - OK
    - Body: Not applicable

### User Authentication

The application uses token-based authentication.

#### Get Authentication Token [/api/auth/login/]

- Method: `POST`
- Permissions: Any user (authentication not required)
- Request Body:
    - `username` (string): User's username.
    - `password` (string): User's password.
- Response:
    - Status Code: 200 - OK
    - Body:
        - `token` (string): Authentication token for the user.
