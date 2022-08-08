import xmlrpc.client

from odoo_auth import backends, settings
from odoo_auth.models import OdooUser


class OdooBackend(backends.OdooBackend):
    def authenticate(self, request, username=None, password=None):
        user = super().authenticate(request, username, password)
        if user and not user.first_name:
            odoo_user = OdooUser.objects.filter(user=user).first()
            if not odoo_user:
                return user
            user_uid = odoo_user.odoo_id

            url = settings.ODOO_SERVER_URL
            if settings.ODOO_SERVER_PORT is None:
                url += f':{settings.ODOO_SERVER_PORT}'
            url = f'{url}/xmlrpc/2/object'

            models = xmlrpc.client.ServerProxy(url)
            data = models.execute_kw(
                'portfolio', user_uid, password, 'res.users', 'search_read',
                [[['login', '=', username]]],
                {
                    'limit': 1,
                    'fields': ['name', 'email'],
                }
            )

            if not len(data):
                return user

            data = data[0]
            if email := data.get('email'):
                user.email = email
            if full_name := data.get('name'):
                name = full_name.split(' ')
                user.last_name = name[0]
                user.first_name = ' '.join(name[1:])
            user.save()
        return user
