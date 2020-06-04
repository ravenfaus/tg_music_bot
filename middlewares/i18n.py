import gettext
import os
from contextvars import ContextVar
from typing import Any, Dict, Tuple

from aiogram.dispatcher.middlewares import BaseMiddleware
from babel.support import LazyProxy

from models import User


class I18nMiddleware(BaseMiddleware):

    ctx_locale = ContextVar('ctx_user_locale', default=None)

    def __init__(self, domain, path=None, default='en'):
        super(I18nMiddleware, self).__init__()

        if path is None:
            path = os.path.join(os.getcwd(), 'locales')

        self.domain = domain
        self.path = path
        self.default = default

        self.locales = self.find_locales()

    def find_locales(self) -> Dict[str, gettext.GNUTranslations]:
        translations = {}

        for name in os.listdir(self.path):
            if not os.path.isdir(os.path.join(self.path, name)):
                continue
            mo_path = os.path.join(self.path, name, 'LC_MESSAGES', self.domain + '.mo')

            if os.path.exists(mo_path):
                with open(mo_path, 'rb') as fp:
                    translations[name] = gettext.GNUTranslations(fp)
            elif os.path.exists(mo_path[:-2] + 'po'):
                raise RuntimeError(f"Found locale '{name} but this language is not compiled!")

        return translations

    def reload(self):
        self.locales = self.find_locales()

    @property
    def available_locales(self) -> Tuple[str]:
        return tuple(self.locales.keys())

    def __call__(self, singular, plural=None, n=1, locale=None) -> str:
        return self.gettext(singular, plural, n, locale)

    def gettext(self, singular, plural=None, n=1, locale=None) -> str:
        if locale is None:
            locale = self.ctx_locale.get()
        if locale not in self.locales:
            if n == 1:
                return singular
            return plural

        translator = self.locales[locale]
        if plural is None:
            return translator.gettext(singular)
        return translator.ngettext(singular, plural, n)

    def lazy_gettext(self, singular, plural=None, n=1, locale=None, enable_cache=False) -> LazyProxy:
        return LazyProxy(self.gettext, singular, plural, n, locale, enable_cache=enable_cache)

    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        *_, data = args
        user: User = data['user']
        data['_'] = self.gettext
        return user.language

    async def trigger(self, action, args):
        if 'update' not in action \
                and 'error' not in action \
                and action.startswith('pre_process'):
            locale = await self.get_user_locale(action, args)
            self.ctx_locale.set(locale)
            return True
