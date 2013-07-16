# -*- coding: utf-8 -*-
import os
import urlparse
import urllib

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, QueryDict
from django.views.defaults import permission_denied
from django.core.files.storage import default_storage
from django.views.defaults import page_not_found
from django.core.urlresolvers import resolve


class LogedInMixin(object):
    need_login = True
    require_admin = False

    def dispatch(self, request, *args, **kwargs):
        if (not settings.LOGIN_PASSWORD or
                request.session.get('loged_in', False) or
                not self.need_login):
            self.is_admin = False
            if not settings.ADMIN_PASSWORD or request.session.get('is_admin', False):
                self.is_admin = True
            elif self.require_admin:
                return permission_denied(request)
            request.session.modified = True
            return super(LogedInMixin, self).dispatch(request, *args, **kwargs)
        else:
            next = request.get_full_path()
            login_url = reverse('fileserver_login')
            login_url_parts = list(urlparse.urlparse(login_url))
            if next:
                querystring = QueryDict(login_url_parts[4], mutable=True)
                querystring['next'] = next
                login_url_parts[4] = querystring.urlencode(safe='/')
            return HttpResponseRedirect(urlparse.urlunparse(login_url_parts))

    def get_context_data(self, **kwargs):
        context = super(LogedInMixin, self).get_context_data(**kwargs)
        context['is_admin'] = self.is_admin
        return context


class SetPathMixin(object):
	
    def get(self, request, *args, **kwargs):
        path = self.get_path()
        if not default_storage.exists(path):
            return page_not_found(request)
        return super(SetPathMixin, self).get(request, *args, **kwargs)

    def get_path(self):
        return urllib.unquote(self.kwargs.get('path', ''))

    def get_context_data(self, **kwargs):
        context = super(SetPathMixin, self).get_context_data(**kwargs)
        path = self.get_path()
        context['path'] = [('', 'index')]
        path_list = path.split(os.sep)
        for index in range(len(path_list)):
            if not path_list[index]:
                continue
            name = path_list[index]
            directory = os.sep.join(path_list[:index + 1])
            context['path'].append((directory, name))
        context['full_path'] = path
        context['active_tab'] = resolve(self.request.path).url_name
        return context
