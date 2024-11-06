#!/bin/bash

# API base URL
BASE_URL="http://localhost:8000/api/v1"

# User credentials
EMAIL="testuser@example.com"
PASSWORD="password123"
NAME="Test User"

# Register the user
echo "Registering the user..."
register_response=$(curl -s -X POST "$BASE_URL/users/register" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"$NAME\", \"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}")
echo "Register response: $register_response"

# Login to get tokens
echo "Logging in to get tokens..."
login_response=$(curl -s -X POST "$BASE_URL/users/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"password\": \"$PASSWORD\"}")

# Extract access and refresh tokens
ACCESS_TOKEN=$(echo "$login_response" | jq -r .access)
REFRESH_TOKEN=$(echo "$login_response" | jq -r .refresh)

echo "Access Token: $ACCESS_TOKEN"
echo "Refresh Token: $REFRESH_TOKEN"

# Verify tokens are retrieved
if [[ -z "$ACCESS_TOKEN" || -z "$REFRESH_TOKEN" ]]; then
  echo "Error: Failed to retrieve access and refresh tokens."
  exit 1
fi

# Create TODO items
echo "Creating TODO items..."
for i in {1..3}; do
  create_response=$(curl -s -X POST "$BASE_URL/tasks" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"title\": \"Task $i\", \"description\": \"Description for Task $i\"}")
  echo "Created TODO $i: $create_response"
done

# Get list of TODOs
echo "Fetching TODO list..."
todo_list=$(curl -s -X GET "$BASE_URL/tasks" \
  -H "Authorization: Bearer $ACCESS_TOKEN")
echo "TODO List: $todo_list"

# Update the first TODO item
TODO_ID=$(echo "$todo_list" | jq -r '.[0].id')
echo "Updating TODO with ID $TODO_ID..."
update_response=$(curl -s -X PUT "$BASE_URL/tasks/$TODO_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Updated Task 1\", \"description\": \"Updated description for Task 1\"}")
echo "Update response: $update_response"

# Change the status of the first TODO item
echo "Updating status of TODO with ID $TODO_ID to COMPLETED..."
status_update_response=$(curl -s -X PATCH "$BASE_URL/tasks/$TODO_ID/status" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"status\": \"COMPLETED\"}")
echo "Status update response: $status_update_response"

# Delete the last TODO item
LAST_TODO_ID=$(echo "$todo_list" | jq -r '.[-1].id')
echo "Deleting TODO with ID $LAST_TODO_ID..."
delete_response=$(curl -s -X DELETE "$BASE_URL/tasks/$LAST_TODO_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN")
echo "Delete response: $delete_response"

# Logout the user by blacklisting the refresh token
echo "Logging out..."
logout_response=$(curl -s -X POST "$BASE_URL/users/logout" \
  -H "Content-Type: application/json" \
  -d "{\"refresh_token\": \"$REFRESH_TOKEN\"}")
echo "Logout response: $logout_response"

echo "API test script completed."
