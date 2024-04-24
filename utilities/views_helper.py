from django.db.models import ProtectedError
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import DestroyModelMixin


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


def remove_unwanted_commas(text):
    """
    This function removes the comma before the pipe (|) and the last comma in a string,
    handling cases with one or two parts.

    Args:
        text: The string to be processed.

    Returns:
        The modified string with the unwanted commas removed.
    """
    # Split the string by the pipe (|) delimiter.
    parts = text.split("|")

    if len(parts) == 1:
        # Handle case with one part: remove only the last comma
        return text.rstrip(",")
    else:
        # Handle case with two parts: remove comma before pipe and last comma
        parts[0] = parts[0].rstrip(",")
        parts[-1] = parts[-1].rstrip(",")

    # Join the parts back together with a pipe (|) delimiter.
    return "|".join(parts)


