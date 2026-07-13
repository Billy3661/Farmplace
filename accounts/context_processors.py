def profile_processor(request):
    context = {}
    if request.user.is_authenticated:
        try:
            context['farmer_profile'] = request.user.profile
        except Exception:
            context['farmer_profile'] = None
    return context
