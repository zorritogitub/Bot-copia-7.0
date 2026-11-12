"""OJS 3.4 Varela submission-file upload. No browser-cookie export or proxy.

Not activated until the copied bot is explicitly configured by its administrator.
"""
import asyncio
import json
import re
from pathlib import Path

import aiohttp
from bs4 import BeautifulSoup

BASE = 'https://revistavarela.uclv.edu.cu/index.php/rv/'
SUBMISSION = 2164
TIMEOUT = aiohttp.ClientTimeout(total=3600, connect=30, sock_connect=30, sock_read=120)


class VarelaError(Exception):
    pass


def _current_user(html):
    match = re.search(r'pkp\.currentUser\s*=\s*(\{[^;]+\})\s*;', html)
    if not match:
        raise VarelaError('No se pudo verificar la sesión autenticada.')
    try:
        obj = json.loads(match.group(1))
        token = obj['csrfToken']
        uid = obj['id']
        if not isinstance(token, str) or not token or not isinstance(uid, int) or uid < 1:
            raise ValueError()
        return uid, token
    except (ValueError, KeyError, TypeError):
        raise VarelaError('No se pudo verificar la sesión autenticada.') from None


def _login_fields(html):
    soup = BeautifulSoup(html, 'html.parser')
    field = soup.find('input', attrs={'name': 'csrfToken'})
    if not field or not field.get('value'):
        raise VarelaError('No se pudo preparar el inicio de sesión.')
    return field['value']


async def upload(path, user, password, *, _base=BASE, _timeout=TIMEOUT):
    """Create a single file in draft 2164; return only confirmed submission-file ID.

    _base and _timeout permit loopback-only mock tests; runtime uses constants.
    On cancellation/timeout after POST, remote outcome is inherently unknown.
    """
    if not user or not password:
        raise VarelaError('Faltan las variables privadas VARELA_USER y VARELA_PASSWORD.')
    path = Path(path)
    if not path.is_file():
        raise VarelaError('El archivo local no existe.')
    async with aiohttp.ClientSession(timeout=_timeout, trust_env=False) as session:
        async with session.get(_base + 'login', allow_redirects=False) as r:
            if r.status != 200:
                raise VarelaError('La página de acceso no está disponible.')
            csrf = _login_fields(await r.text())
        # Never log credentials, token, payload or response bodies. No redirects on POST.
        async with session.post(_base + 'login/signIn', allow_redirects=False, data={
            'csrfToken': csrf, 'source': '', 'username': user, 'password': password,
        }) as r:
            if r.status not in (200, 302, 303):
                raise VarelaError('No se pudo iniciar sesión en la revista.')
            login_result = await r.text() if r.status == 200 else ''
        # Verify identity using a protected page, not the login redirect. A widget
        # in the login form alone does not prove the server requires a challenge.
        async with session.get(_base + 'submission', params={'id': SUBMISSION}, allow_redirects=False) as r:
            page = await r.text() if r.status == 200 else ''
            try:
                if r.status != 200:
                    raise VarelaError('Sesión no disponible.')
                uid, csrf = _current_user(page)
            except VarelaError:
                # Only identify a CAPTCHA rejection if a visible error says so.
                text = BeautifulSoup(login_result, 'html.parser').get_text(' ', strip=True)
                if re.search(r'(captcha|recaptcha).{0,100}(incorrect|inválid|invalid|error|requerid|obligatori|failed)|(incorrect|inválid|invalid|error|requerid|obligatori|failed).{0,100}(captcha|recaptcha)', text, re.I):
                    raise VarelaError('La revista rechazó el inicio de sesión por CAPTCHA; se necesita validación legítima.') from None
                raise VarelaError('Inicio de sesión rechazado o sesión no disponible; no se reintentó.') from None
        async with session.get(_base + f'api/v1/submissions/{SUBMISSION}', allow_redirects=False) as r:
            if r.status != 200:
                raise VarelaError('No se puede acceder al borrador autorizado.')
            try:
                submission = await r.json(content_type=None)
            except (ValueError, aiohttp.ContentTypeError):
                raise VarelaError('Respuesta de borrador inválida.') from None
        if (not isinstance(submission, dict) or submission.get('id') != SUBMISSION
                or not submission.get('submissionProgress')):
            raise VarelaError('El envío no es un borrador editable; se detuvo la carga.')
        if submission.get('dateSubmitted'):
            raise VarelaError('El registro indica fecha de envío pese a figurar en progreso; se detuvo la carga hasta aclarar su estado.')
        # One-part multipart, streamed by aiohttp; OJS uses the default genre when allowed.
        form = aiohttp.FormData()
        form.add_field('fileStage', '2')
        with path.open('rb') as stream:
            form.add_field('file', stream, filename=path.name, content_type='application/octet-stream')
            async with session.post(_base + f'api/v1/submissions/{SUBMISSION}/files',
                                    data=form, headers={'X-Csrf-Token': csrf}, allow_redirects=False) as r:
                status = r.status
                try:
                    result = await r.json(content_type=None)
                except (ValueError, aiohttp.ContentTypeError):
                    result = None
        if status != 200:
            raise VarelaError(f'La revista rechazó la carga (HTTP {status}); revisa formato, tamaño y categoría.')
        if (not isinstance(result, dict) or not isinstance(result.get('id'), int)
                or result['id'] < 1 or result.get('submissionId') != SUBMISSION
                or result.get('fileStage') != 2 or result.get('uploaderUserId') != uid):
            raise VarelaError('Respuesta incompleta: no se puede confirmar la carga; revisa el borrador antes de reintentar.')
        return result['id']


def _captcha_rejected(html):
    """Visible error text is evidence of a challenge; widget markup alone is not."""
    text = BeautifulSoup(html, 'html.parser').get_text(' ', strip=True)
    return bool(re.search(
        r'(captcha|recaptcha).{0,100}(incorrect|inválid|invalid|error|requerid|obligatori|failed)'
        r'|(incorrect|inválid|invalid|error|requerid|obligatori|failed).{0,100}(captcha|recaptcha)',
        text, re.I))


async def diagnostic(user, password, *, _base=BASE):
    """Read-only journal diagnostic. One login POST max, no mutations or uploads.

    Output is an allowlisted fixed-format report, never response content, headers,
    exception text, tokens, cookies or credentials. GET authorization does not
    establish upload permission. The caller must restrict access to the admin.
    """
    if not user or not password:
        return 'Faltan credenciales privadas de Varela en Render.'
    result = []
    phase = 'acceso'
    try:
        timeout = aiohttp.ClientTimeout(total=45, connect=15, sock_connect=15, sock_read=20)
        async with aiohttp.ClientSession(timeout=timeout, trust_env=False) as session:
            async with session.get(_base + 'login', allow_redirects=False) as r:
                result.append(f'Conexión: HTTP {int(r.status)}')
                if r.status != 200:
                    return '\n'.join(result + ['No se pudo preparar el acceso.'])
                try:
                    csrf = _login_fields(await r.text())
                except VarelaError:
                    return '\n'.join(result + ['No se encontró el formulario de acceso.'])
            phase = 'inicio de sesión'
            async with session.post(_base + 'login/signIn', allow_redirects=False, data={
                'csrfToken': csrf, 'source': '', 'username': user, 'password': password,
            }) as r:
                result.append(f'Inicio de sesión: HTTP {int(r.status)}')
                login_result = await r.text() if r.status == 200 else ''
                sign_status = r.status
            if sign_status not in (200, 302, 303):
                return '\n'.join(result + ['Autenticación no confirmada; no se reintentó.'])
            phase = 'verificación de sesión'
            async with session.get(_base + 'submission', params={'id': SUBMISSION}, allow_redirects=False) as r:
                result.append(f'Página protegida: HTTP {int(r.status)}')
                page = await r.text() if r.status == 200 else ''
                try:
                    if r.status != 200:
                        raise VarelaError('no')
                    _current_user(page)
                except VarelaError:
                    if _captcha_rejected(login_result):
                        result.append('CAPTCHA requerido o rechazado; requiere validación legítima.')
                    else:
                        result.append('Autenticación no confirmada; rechazo o sesión no disponible.')
                    return '\n'.join(result)
            result.append('Autenticación: confirmada.')
            phase = 'lectura del borrador'
            async with session.get(_base + f'api/v1/submissions/{SUBMISSION}', allow_redirects=False) as r:
                result.append(f'Lectura del registro 2164: HTTP {int(r.status)}')
                if r.status != 200:
                    result.append('Lectura restringida o no disponible; permisos de carga no verificados.')
                    return '\n'.join(result)
                try:
                    submission = await r.json(content_type=None)
                except (ValueError, aiohttp.ContentTypeError):
                    return '\n'.join(result + ['Respuesta del registro inválida.'])
            if not isinstance(submission, dict) or submission.get('id') != SUBMISSION:
                return '\n'.join(result + ['No se confirmó el registro solicitado.'])
            # Do not echo arbitrary server strings: only known progress values.
            progress = submission.get('submissionProgress')
            known = ('start', 'upload', 'metadata', 'confirmation', 'complete')
            if not progress:
                progress = 'vacío o ausente'
            elif not isinstance(progress, str) or progress not in known:
                progress = 'otro (no publicado)'
            submitted = ('presente' if submission.get('dateSubmitted') else 'ausente')
            result.extend([f'Progreso: {progress}', f'Fecha de envío: {submitted}',
                           'Lectura permitida; permisos de carga no verificados.',
                           'Sin cargas ni cambios en el borrador.'])
            if submission.get('dateSubmitted'):
                result.append('La protección existente impide subir mientras se aclara la fecha.')
            return '\n'.join(result)
    except (asyncio.TimeoutError, aiohttp.ClientError):
        return '\n'.join(result + [f'Error de red o tiempo agotado durante {phase}; no se reintentó.'])
    except Exception:
        # No exception interpolation or logging: network exceptions can contain secrets.
        return '\n'.join(result + [f'No se pudo completar el diagnóstico durante {phase}.'])
