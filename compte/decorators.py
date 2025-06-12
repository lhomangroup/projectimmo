from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('acceuil')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			# Pour le modèle Account personnalisé, on peut utiliser d'autres critères
			# Par exemple, vérifier si l'utilisateur a un Client associé
			if hasattr(request.user, 'client') and 'customer' in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You are not authorized to view this page')
		return wrapper_func
	return decorator

def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		# Utiliser les attributs du modèle Account personnalisé
		if request.user.is_admin or request.user.is_superuser:
			return view_func(request, *args, **kwargs)
		elif hasattr(request.user, 'client'):
			return redirect('user-page')
		else:
			return HttpResponse('You are not authorized to view this page')

	return wrapper_function