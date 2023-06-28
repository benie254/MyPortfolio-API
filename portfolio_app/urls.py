from django.urls import path,re_path as url 
from portfolio_app import views 

urlpatterns = [
    # all users
    path('',views.home,name="home"),
    url(r'^projects/all$',views.AllProjects.as_view(),name="all-projects"),
    url(r'^projects/featured$',views.FeaturedProjects.as_view(),name="featured-projects"),
    url(r'^project/pinned$',views.PinnedProjects.as_view(),name="pinned-project"),
    url(r'^project/details/(\d+)$',views.ProjectDetails.as_view(),name="project-details"),
    url(r'^project/likes/(\d+)$',views.ProjectLikes.as_view(),name="project-likes"),
    url(r'^project/comments/(\d+)$',views.ProjectComments.as_view(),name="project-comments"),
    url(r'^comments/all$',views.AllComments.as_view(),name="all-comments"),
    url(r'^comment/details/(\d+)$',views.CommentDetails.as_view(),name="comment-details"),
    url(r'^likes/all$',views.AllLikes.as_view(),name="all-likes"),
    url(r'^like/details/(\d+)$',views.LikeDetails.as_view(),name="like-details"),
    url(r'^contacts/add$',views.AddContact.as_view(),name="add-contacts"),
    # authenticated users
    url(r'^projects/add$',views.AddProject.as_view(),name="add-project"),
    url(r'^project/update/(\d+)$',views.UpdateProject.as_view(),name="update-project"),
    url(r'^comment/delete/(\d+)$',views.DeleteComment.as_view(),name="delete-comment"),
    url(r'^like/delete/(\d+)$',views.DeleteLike.as_view(),name="delete-like"),    
    url(r'^contacts/all$',views.AllContacts.as_view(),name="all-contacts"),
    url(r'^contact/details/(\d+)$',views.ContactDetails.as_view(),name="contact-details"),
    url(r'^contact/delete/(\d+)$',views.DeleteContact.as_view(),name="delete-contact"),    
]