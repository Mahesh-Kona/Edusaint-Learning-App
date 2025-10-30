# Postman collection

A Postman collection for common API requests is included at the repository root: `postman_collection.json`.

How to import
1. Open Postman
2. File -> Import -> Choose Files -> select `postman_collection.json`
3. The collection will appear in the sidebar. Edit the request URLs if your backend runs on a non-default host/port.

Auth note
- To test protected endpoints, copy an `access_token` returned by the Login or Register request and add an `Authorization` header to subsequent requests with the value `Bearer <access_token>`.

Typical requests included
- Register
- Login
- Refresh token
- List courses
- Get lesson content
