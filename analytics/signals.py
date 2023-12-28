from django.dispatch import Signal

# object_viewed_signal = Signal('instance', 'request')  # not accepted in django 4.0
object_viewed_signal = Signal()