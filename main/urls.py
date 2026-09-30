from django.urls import path


from main.views import (
    show_main,
    show_experience,
    show_education,
    create_education,
    create_experience,
    get_education_json,
    get_experience_json,
    delete_experience,
    delete_education,
    show_previous_work,
    create_previous_work,
    get_previous_work_json,
    delete_previous_work,
    update_experience,
    update_education,
    update_previous_work,
    register,
    login_user,
    logout_user,
    toggle_star_experience,
    toggle_star_education,
    toggle_star_previouswork,
    show_profile,
    create_experience_ajax
)

app_name = "main"
urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("education/", show_education, name="show_education"),
    path("PreviousWork/", show_previous_work, name="show_previous_work"),
    path("education/add/", create_education, name="create_education"),
    path("experience/add/", create_experience, name="create_experience"),
    path("PreviousWork/add/", create_previous_work, name="create_previous_work"),
    path("api/educations/", get_education_json, name="get_educations_json"),
    path("api/experiences/", get_experience_json, name="get_experience_json"),
    path("api/previouswork/", get_previous_work_json, name="get_previous_work_json"),
    path("experience/delete/<uuid:experience_id>/",delete_experience,name="delete_experience",),
    path("education/delete/<int:education_id>/",delete_education,name="delete_education",),
    path("PreviousWork/delete/<int:previous_work_id>/",delete_previous_work,name="delete_previous_work",),
    path("experience/edit/<uuid:experience_id>/", update_experience,name="update_experience",),
    path("education/edit/<int:education_id>/",update_education, name="update_education",),
    path("previous-work/edit/<int:previous_work_id>/",update_previous_work,name="update_previous_work",),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("experience/<uuid:experience_id>/star/",toggle_star_experience,name="toggle_star_experience",),
    path("education/<int:education_id>/star/",toggle_star_education,name="toggle_star_education"),
    path("previous-work/<int:previouswork_id>/star/",toggle_star_previouswork,name="toggle_star_previouswork"),
    path("profile/<str:username>/",show_profile,name="show_profile"),
    path("experience/add-ajax/", create_experience_ajax, name="create_experience_ajax"),

]