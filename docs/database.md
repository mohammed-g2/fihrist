Relationships
```
User 1---* Post
User *---1 Role
User 1---1 Blog
Blog 1---* Posts
Blog *---* BlogMember
User 1---1 BlogMember
Post *---1 Category
Post 1---* Comment
Post 1---* Revisions
Post 1---1 PostImage
User 1---* PostImage
```

User (author/owner)
- id
- username
- email
- password_hash
- member_since
- last_seen
- avatar_hash
- role_id* 

Role
- id
- name (banned/author/moderator/admin)
- permissions
- default

Blog
- id
- name
- slug
- description
- created_at
- user_id*

BlogMember
- id
- blog_id*
- user_id*
- role (owner/writer)

Post
- id
- blog_id*
- user_id*
- title
- slug
- content
- status (draft/published)
- created_at
- updated_at

PostImage
- id 
- post_id*
- user_id*
- url
- thumbnail_url
- alt_text
- caption
- order (for multiple images)
- created_at

Revisions
- id
- post_id
- title
- content
- created_at

Category
- id
- name
- slug

Comment
- id
- post_id*
- user_id*
- content
- created_at
- approved
