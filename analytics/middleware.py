import time
import json
import logging
from .models import SecurityEvent

logger = logging.getLogger('api')

class SecurityLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        # Log API requests
        if request.path.startswith('/api/'):
            self._log_api_request(request, response, start_time)
        
        # Log security events
        if request.path.startswith('/simulations/track/'):
            try:
                SecurityEvent.objects.create(
                    event_type='phishing_click',
                    user_ip=self.get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                    details={
                        'path': request.path,
                        'method': request.method,
                        'response_time': round(time.time() - start_time, 3),
                        'user_agent_short': request.META.get('HTTP_USER_AGENT', '')[:100],
                    }
                )
            except Exception as e:
                logger.error(f"Security logging error: {e}")
        
        # Log admin access
        elif request.path.startswith('/admin/'):
            try:
                SecurityEvent.objects.create(
                    event_type='admin_login',
                    user_ip=self.get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                    details={
                        'path': request.path,
                        'method': request.method,
                        'user': getattr(request.user, 'username', 'anonymous'),
                    }
                )
            except Exception as e:
                logger.error(f"Admin logging error: {e}")
        
        return response

    def _log_api_request(self, request, response, start_time):
        """Log API requests for monitoring and security"""
        try:
            log_data = {
                'timestamp': time.time(),
                'method': request.method,
                'path': request.path,
                'user': getattr(request.user, 'username', 'anonymous'),
                'status_code': response.status_code,
                'response_time': round(time.time() - start_time, 3),
                'user_agent': request.META.get('HTTP_USER_AGENT', '')[:200],
                'ip_address': self.get_client_ip(request),
            }
            
            # Log sensitive operations
            if request.method in ['POST', 'PUT', 'DELETE'] and '/api/' in request.path:
                logger.info(f"API Modification: {log_data}")
            else:
                logger.debug(f"API Access: {log_data}")
                
        except Exception as e:
            logger.error(f"API logging error: {e}")

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
