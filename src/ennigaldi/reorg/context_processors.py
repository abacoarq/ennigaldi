def current_batch(request):
    from .models import Batch
    active = Batch.objects.filter(active=True).first()
    if active:
        return {'active': active.__str__()}
    else:
        return {'active': 'No active batch.'}
