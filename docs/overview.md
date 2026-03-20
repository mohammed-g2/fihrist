## pages

### Public
- home
- post
- post list by date/category

### Non logged in Users
- register
- login
- forgot password

### Registered Users
- profile
- user settings
- new blog

### Blog Owner
- workspace
- new post
- edit post
- blog settings

### Moderator
- moderator dashboard
- posts list
- comments list

### Admin
- admin dashboard
- categories list
- users list
- website settings (* work in progress)

---

## Features

### User Authentication
- register new account
- login
- logout
- role system (admin - moderator - user - banned) 

### Blog Management
- owner can  edit blog settings
- owner can add posts to blog
- only blog owner can edit or delete published posts
- switch posts between published (making it public) and draft (private)

### Post Management
- create post
- attach image to a post
- edit post
- delete post
- publish / draft
- snapshots of posts are kept for rollback (* work in progress)

### Content Organization
- create/edit/delete categories

### Comments
- guests (unregistered users) can add comments (* not implemented)
- add comment
- moderate comment
- delete comment

### Moderators
- list posts
- list comments
- delete posts
- delete comments
- ban users (for a time) (* work in progress)
 
### Admin Dashboard
- list posts
- list users
- list comments
- delete users
- delete comments
- ban users (* work in progress)
- add moderators

### Public Pages
- home page (recent posts)
- single post page
- list posts by category page
- list posts by date page (* work in progress)
- about us

### Advanced Features
- search (* work in progress)
- pagination
- markdown support
- image upload
- scheduled publishing
- revision history

### Other
- Rate Limiting (* not implemented)
- Caching Layer (* not implemented)

### Future
- owners can add css theme to the blog
- post can have multiple images
- featured images section
- activity page for user (blog limited)
- activity page for admin (website)
