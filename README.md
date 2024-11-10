# User and Article API

This API manages user and article data, providing authentication, registration, and CRUD operations for users and articles.

## User Endpoints

### Get Authenticated User

- **Endpoint**: `GET /logged-in`
- **Description**: Returns the currently authenticated user.
- **Response**: `200 OK`

### Register a New User

- **Endpoint**: `POST /signup`
- **Description**: Registers a new user.
- **Status**: `201 Created`
- **Errors**: `409 Conflict` if the email is already registered.

### List All Users

- **Endpoint**: `GET /`
- **Description**: Returns a list of all users.
- **Response**: `200 OK`

### Get User Details

- **Endpoint**: `GET /{user_id}`
- **Description**: Returns details for a specific user by ID.
- **Status**: `200 OK`
- **Errors**: `404 Not Found` if the user is not found.

### Update User

- **Endpoint**: `PUT /{user_id}`
- **Description**: Updates user details by ID.
- **Status**: `202 Accepted`
- **Errors**: `404 Not Found` if the user is not found.

### Delete User

- **Endpoint**: `DELETE /{user_id}`
- **Description**: Deletes a user by ID.
- **Status**: `204 No Content`
- **Errors**: `404 Not Found` if the user is not found.

### Login

- **Endpoint**: `POST /login`
- **Description**: Authenticates a user and returns an access token.
- **Status**: `200 OK`
- **Errors**: `400 Bad Request` if credentials are invalid.

## Article Endpoints

### Create an Article

- **Endpoint**: `POST /`
- **Description**: Creates a new article associated with the authenticated user.
- **Status**: `201 Created`

### List All Articles

- **Endpoint**: `GET /`
- **Description**: Returns all articles.
- **Response**: `200 OK`

### Get Article Details

- **Endpoint**: `GET /{article_id}`
- **Description**: Returns details for a specific article by ID.
- **Status**: `200 OK`
- **Errors**: `404 Not Found` if the article is not found.

### Update an Article

- **Endpoint**: `PUT /{article_id}`
- **Description**: Updates an article by ID.
- **Status**: `202 Accepted`
- **Errors**: `404 Not Found` if the article is not found.

### Delete an Article

- **Endpoint**: `DELETE /{article_id}`
- **Description**: Deletes a specific article for the authenticated user.
- **Status**: `204 No Content`
- **Errors**: `404 Not Found` if the article is not found or `401 Unauthorized` if the user lacks permission.

## Dependencies

- `get_session`: Dependency for retrieving an async database session.
- `get_current_user`: Dependency for retrieving the current authenticated user.

## Authentication

- The API uses token-based authentication, generated through the `/login` endpoint.

## Security

- **Password**: Passwords are hashed before storing in the database.
- **Authorization**: Only the authenticated user can create, update, and delete their articles.

## Common Errors

- `409 Conflict`: Email already registered.
- `404 Not Found`: User or article not found.
- `400 Bad Request`: Invalid login credentials.
- `401 Unauthorized`: Unauthorized access to resources.

## Example Workflow

1. Register a user via `/signup`.
2. Log in via `/login` to receive an access token.
3. Use the token to perform protected operations, such as creating, updating, and deleting articles.

