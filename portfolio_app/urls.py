from django.urls import path,re_path as url 
from portfolio_app import views 

urlpatterns = [
    # all users
    path('',views.home,name="home"),
    url(r'^projects/all$',views.AllProjects.as_view(),name="all-projects"),
    url(r'^project/details/(\d+)$',views.ProjectDetails.as_view(),name="project-details"),
    url(r'^project/likes$',views.ProjectLikes.as_view(),name="project-likes"),
    url(r'^project/comments$',views.ProjectComments.as_view(),name="project-comments"),
    url(r'^technologies/all$',views.AllTechnologies.as_view(),name="all-technologies"),
    url(r'^technology/details/(\d+)$',views.TechnologyDetails.as_view(),name="technology-details"),
    url(r'^features/all$',views.AllFeatures.as_view(),name="all-features"),
    url(r'^feature/details/(\d+)$',views.FeatureDetails.as_view(),name="feature-details"),
    url(r'^comments/all$',views.AllComments.as_view(),name="all-coments"),
    url(r'^comment/details/(\d+)$',views.CommentDetails.as_view(),name="comment-details"),
    url(r'^likes/all$',views.AllLikes.as_view(),name="all-likes"),
    url(r'^like/details/(\d+)$',views.LikeDetails.as_view(),name="like-details"),
    # authenticated users
    url(r'^projects/add$',views.AddProject.as_view(),name="add-project"),
    url(r'^project/update/(\d+)$',views.UpdateProject.as_view(),name="update-project"),
    url(r'^technologies/add$',views.AddTechnology.as_view(),name="add-technology"),
    url(r'^technology/update/(\d+)$',views.UpdateTechnology.as_view(),name="update-technology"),
    url(r'^features/add$',views.AddFeature.as_view(),name="add-feature"),
    url(r'^feature/update/(\d+)$',views.UpdateFeature.as_view(),name="update-feature"),
    url(r'^comment/delete/(\d+)$',views.DeleteComment.as_view(),name="delete-comment"),
    url(r'^contacts/all$',views.AllContacts.as_view(),name="all-contacts"),
    url(r'^contacts/add$',views.AddContact.as_view(),name="add-contacts"),
    url(r'^contact/details/(\d+)$',views.ContactDetails.as_view(),name="contact-details"),
]