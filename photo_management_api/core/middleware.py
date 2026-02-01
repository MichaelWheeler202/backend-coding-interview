from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status

class LoginRequiredMiddleware(MiddlewareMixin):
    exempted_paths = [
        '/admin/login',
        '/github_sso/login',
        '/github_sso/callback',
    ]

    def __init__(self, get_response=None):
        super().__init__(get_response)
        # build trie once per middleware instance
        self._exempted_trie = self._build_trie(self.exempted_paths)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not self._path_exempt(self._exempted_trie, request.path) and not request.user.is_authenticated:
            return HttpResponse("You must be signed in with github SSO to access this endpoint.", status=status.HTTP_401_UNAUTHORIZED)

        return None

    @staticmethod
    def _build_trie(paths):
        trie = {}
        for p in paths:
            node = trie
            for ch in p:
                node = node.setdefault(ch, {})
            node[''] = True  # terminal marker
        return trie

    @staticmethod
    def _path_exempt(trie, path):
        node = trie
        # if an exempted path is empty string (unlikely) it's handled by terminal marker at root
        if '' in node:
            return True
        for ch in path:
            if ch in node:
                node = node[ch]
                if '' in node:
                    # found a terminal marker for an exempted prefix
                    return True
            else:
                return False
        # path consumed; exempt if terminal marker at current node
        return '' in node