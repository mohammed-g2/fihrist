## endpoint structure

Endpoint                         Methods    Rule                         
-------------------------------  ---------  -----------------------------
Admin Blueprint                                                            <br />
admin.admin_dashboard            GET        /admin/admin-dashboard         <br />   
admin.manage_categories          GET, POST  /admin/manage-categories       <br />   
admin.moderate_comments          GET, POST  /admin/moderate-comments       <br />   
admin.moderate_posts             GET, POST  /admin/moderate-posts          <br />  
admin.moderator_dashboard        GET        /admin/moderator-dashboard     <br />
---
Authentication Blueprint                                                   <br />
auth.confirm                     GET        /auth/confirm-account/<token>  <br />
auth.login                       GET, POST  /auth/login                    <br />
auth.logout                      GET        /auth/logout                   <br />
auth.register                    GET, POST  /auth/register                 <br />
auth.request_confirmation_email  GET        /auth/confirm-account          <br />
auth.request_password_reset      GET, POST  /auth/reset-password           <br />
auth.reset_password              GET, POST  /auth/reset-password/<token>   <br />
---
Blog Blueprint                                                             <br />
blog.blank                       GET        /blog/blank                    <br />
blog.change_post_status          POST       /blog/post/status/<int:id>     <br />
blog.create                      GET, POST  /blog/create                   <br />
blog.create_comment              POST       /blog/create-comment           <br />
blog.create_post                 GET, POST  /blog/create-post              <br />
blog.delete_comment              POST       /blog/delete-comment/<int:id>  <br />
blog.delete_post                 POST       /blog/post/delete/<int:id>     <br />
blog.edit_post                   GET, POST  /blog/edit-post/<int:id>       <br />
blog.get_post                    GET        /blog/post/<slug>              <br />
blog.index                       GET        /blog/                         <br />
blog.workspace                   GET        /blog/workspace                <br />
---
Main Blueprint                                                             <br />
main.get_by_category             GET        /<slug>                        <br />
main.index                       GET        /                              <br />
main.set_language                GET        /translate/<lang>              <br />
---
User Blueprint                                                             <br />
user.change_password             GET, POST  /user/change-password/<token>  <br />
user.profile                     GET        /user/profile/<username>       <br />
user.settings                    GET, POST  /user/settings                 <br />
user.update_email                GET        /user/update-email/<token>     <br />
---
Other                                                                      <br />
static                           GET        /static/<path:filename>        <br />
