import socket

import falcon


class HealthCheck:
    def on_get(self, request, response):
        hostname = socket.gethostname()

        health_response = \
                    {
                        'data':
                        {
                            'status': 'healthy',
                            'hostname': hostname
                        }
                    }

        response.media = health_response
        response.status = falcon.HTTP_200
