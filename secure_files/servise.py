def get_user_image(user, request):
    """Return correct image based on user role"""

    try:
        if hasattr(user, "employee") and user.employee and user.employee.photo:
            return request.build_absolute_uri(user.employee.photo.url)

        if hasattr(user, "teamlead") and user.teamlead and user.teamlead.photo:
            return request.build_absolute_uri(user.teamlead.photo.url)

        if hasattr(user, "hr") and user.hr and user.hr.photo:
            return request.build_absolute_uri(user.hr.photo.url)

        if hasattr(user, "accountent") and user.accountent and user.accountent.photo:
            return request.build_absolute_uri(user.accountent.photo.url)

        if hasattr(user, "organisation_admin") and user.organisation_admin and user.organisation_admin.photo:
            return request.build_absolute_uri(user.organisation_admin.photo.url)

        if hasattr(user, "profile_image") and user.profile_image:
            return request.build_absolute_uri(user.profile_image.url)

    except Exception:
        pass

    return None

