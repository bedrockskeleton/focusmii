def get_selected_theme(user):
    try:
        return user.profile.selected_theme
    except AttributeError:
        return None