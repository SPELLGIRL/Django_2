from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from authapp.models import CustomUser
from adminapp.models.users import UserEditForm
from django.urls import reverse_lazy


class UserUpdateView(UpdateView):
    model = CustomUser
    template_name = 'adminapp/users/update.html'
    success_url = reverse_lazy('admin:users')
    form_class = UserEditForm

    def get_context_data(self, **kwargs):
        parent_context = super(UserUpdateView, self).get_context_data(**kwargs)
        parent_context['title'] = 'Update user'

        return parent_context

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)
