# from django.shortcuts import redirect
# from .models import UserSubscription

# def subscription_required(view_func):
#     def _wrapped_view(request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return redirect('login')  

        
#         if not UserSubscription.objects.filter(user=request.user, is_active=True).exists():
#             return redirect('subscribe') 

#         return view_func(request, *args, **kwargs)  

#     return _wrapped_view
