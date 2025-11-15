# Инструкция по настройке OAuth Redirect URI

## Проблема: redirect_uri_mismatch

Если вы получаете ошибку `redirect_uri_mismatch`, это означает, что redirect URI, который использует приложение, не зарегистрирован в консоли OAuth провайдера.

## Решение

### Google Cloud Console

1. Откройте [Google Cloud Console](https://console.cloud.google.com/)
2. Выберите ваш проект
3. Перейдите в **APIs & Services** → **Credentials**
4. Найдите ваше OAuth 2.0 Client ID и нажмите на него для редактирования
5. В разделе **Authorized redirect URIs** добавьте **ОБА** следующих URI:
   ```
   http://localhost:8000/accounts/google/login/callback/
   http://127.0.0.1:8000/accounts/google/login/callback/
   ```
6. Нажмите **Save**

### Yandex OAuth

1. Откройте [Yandex OAuth](https://oauth.yandex.ru/)
2. Перейдите в раздел **Мои приложения**
3. Выберите ваше приложение
4. В разделе **Redirect URI** добавьте **ОБА** следующих URI:
   ```
   http://localhost:8000/accounts/yandex/login/callback/
   http://127.0.0.1:8000/accounts/yandex/login/callback/
   ```
5. Сохраните изменения

## Почему нужны оба URI?

Браузер может использовать либо `localhost`, либо `127.0.0.1` в зависимости от настроек DNS и операционной системы. Чтобы избежать ошибок, нужно зарегистрировать оба варианта.

## После настройки

После добавления redirect URI в консоли провайдера:
1. Подождите несколько минут (изменения могут применяться не мгновенно)
2. Перезапустите Django сервер
3. Попробуйте войти через OAuth снова

