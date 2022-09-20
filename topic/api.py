import json

from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render

from core.models import Task


def add_tag(request, taskId):

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        task = get_object_or_404(Task, id=taskId)

        if request.method == 'PUT':
            data = json.load(request)
            updated_values = data.get('payload')
            
            if task.tags:
                tag_set = set(task.tags.split(","))
                tag_set.add(updated_values['tags'])
                task.tags = ','.join(tag for tag in tag_set)
            else:
                task.tags = updated_values['tags'] 
            
            task.save()

            return JsonResponse({'status': 'Tags updated!'})

    return HttpResponseBadRequest('Invalid request')

def remove_tag(request, taskId):

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        task = get_object_or_404(Task, id=taskId)

        if request.method == 'PUT':
            data = json.load(request)
            deleted_value = data.get('payload')
            tags = task.tags.split(",")
            tags.remove(deleted_value['tags'])
            
            if tags:
                task.tags = ",".join(tags) 
            else:
                task.tags = None
            
            task.save()

            return JsonResponse({'status': 'Tags remove!'})

    return HttpResponseBadRequest('Invalid request')




def update_font_size(request, taskId):

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        task = get_object_or_404(Task, id=taskId)

        if request.method == 'PUT':
            data = json.load(request)
            task.font_size = data.get('font_size')
            task.save()

            return JsonResponse({'status': 'Font Size updated!'})

    return HttpResponseBadRequest('Invalid request')
