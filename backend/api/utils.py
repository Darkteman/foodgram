from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response


def create_relations(request, obj, related_model, name_serializer, field):
    """
    Универсальная функция для создания связей между моделями.
    """
    kwargs = record_kwargs(request, obj, field)
    created_obj, created = related_model.objects.get_or_create(**kwargs)
    if created:
        serializer = name_serializer(obj, context={'request': request})
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)
    return Response({"errors": "Связь уже существует!"},
                    status=status.HTTP_400_BAD_REQUEST)


def delete_relations(request, id, model, related_model, field):
    """
    Универсальная функция для удаления связей между моделями.
    """
    obj = get_object_or_404(model, id=id)
    kwargs = record_kwargs(request, obj, field)
    try:
        related_model.objects.get(**kwargs).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        return Response({"errors": "Отсутствует предварительная связь!"},
                        status=status.HTTP_400_BAD_REQUEST)


def record_kwargs(request, obj, field):
    """
    Формирование словаря для передачи в менеджер модели.
    """
    kwargs = {}
    kwargs['user'] = request.user
    kwargs[field] = obj
    return kwargs
