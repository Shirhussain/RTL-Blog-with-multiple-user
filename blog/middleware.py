from .models import IPAddress


class IPAddressMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        
        # geting the IP address of user with x_forward_for
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            # the best way for geting ip address of user is by 'x_forwared_for' but if we can't find
            # so you can get with 'REMOTE_ADDR' but it's not so recommended
            ip = request.META.get('REMOTE_ADDR')
        
        try:
            ip_address = IPAddress.objects.get(ip_address=ip)
        except IPAddress.DoesNotExist:
            ip_address = IPAddress(ip_address=ip)
            ip_address.save()
        request.user.ip_address = ip_address

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response