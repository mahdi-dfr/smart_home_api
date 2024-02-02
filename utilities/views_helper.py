from django.db.models import ProtectedError
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import DestroyModelMixin

from setting.models import Log


class SavingByRoleMixin:
    """
    This mixin class used in ViewSets,
    we override perform_create() and perform_update().
    this class prevent from duplicate role check in saving objects.
    """

    def _perform_by_role(self, serializer):
        _user = self.request.user

        # if province_office try to save an object. that object must be in same province automatically.
        if _user.role == '2':
            # the province_office must have province
            if _user.province:
                return serializer.save(province=_user.province)
            else:
                raise ValidationError('استانی برای شما تعریف نشده است!')

        return serializer.save()

    def perform_create(self, serializer):
        return self._perform_by_role(serializer)

    def perform_update(self, serializer):
        return self._perform_by_role(serializer)


class DestroyProtectedMixin(DestroyModelMixin):
    """
    When we want to delete a protected object. it has potential to raise ProtectedError exception.
    This class should only be used together with the DestroyMixin class.
    """

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            raise ValidationError('این مورد به دلیل استفاده شدن توسط دیگر اشیا قابل حذف نیست!')


class LogActivityMixin:
    def log_activity(self, action, details=None):
        user = self.request.user
        Log.objects.create(user=user, action=action, details=details)


class CreateUpdateMixin(LogActivityMixin):
    def perform_create(self, serializer):
        self.log_activity('create data in:  Model')
        serializer.save()

    def perform_update(self, serializer):
        self.log_activity('update data in:  Model')
        serializer.save()

    def perform_destroy(self, instance):
        self.log_activity('delete data in : Model')
        instance.delete()
