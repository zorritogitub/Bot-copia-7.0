import asyncio
import unittest
from unittest.mock import patch
import varela_client as c
from test_varela import Session, Response

class DiagSession(Session):
    def get(self, url, **kw):
        if self.variant == 'timeout' and url.endswith('/login'):
            raise asyncio.TimeoutError('secret error must not appear')
        if self.variant == 'restricted' and url.endswith('/api/v1/submissions/2164'):
            self.calls.append('draft'); return Response(status=403)
        return super().get(url, **kw)

class Tests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        Session.calls=[]; DiagSession.calls=Session.calls; DiagSession.variant='ok'
        self.p=patch.object(c.aiohttp, 'ClientSession', DiagSession);self.p.start()
    async def asyncTearDown(self): self.p.stop()
    async def run_diag(self): return await c.diagnostic('sensitive_user','sensitive_password')
    async def test_success(self):
        s=await self.run_diag()
        self.assertIn('Autenticación: confirmada',s); self.assertIn('Fecha de envío: ausente',s)
        self.assertEqual(Session.calls,['login','sign','page','draft'])
        for secret in ('sensitive_user','sensitive_password','auth','cs'): self.assertNotIn(secret,s)
    async def test_captcha_markup_not_rejection(self):
        DiagSession.variant='captcha';s=await self.run_diag();self.assertIn('Autenticación: confirmada',s)
        self.assertNotIn('CAPTCHA requerido',s)
    async def test_captcha_rejection(self):
        DiagSession.variant='captcha_rejected';s=await self.run_diag();self.assertIn('CAPTCHA requerido',s)
        self.assertEqual(Session.calls,['login','sign','page'])
    async def test_timeout(self):
        DiagSession.variant='timeout';s=await self.run_diag();self.assertIn('tiempo agotado',s);self.assertNotIn('secret',s)
        self.assertEqual(Session.calls,[])
    async def test_restricted(self):
        DiagSession.variant='restricted';s=await self.run_diag();self.assertIn('HTTP 403',s);self.assertIn('restringida',s)
        self.assertEqual(Session.calls,['login','sign','page','draft'])
    async def test_ambiguous(self):
        DiagSession.variant='ambiguous';s=await self.run_diag();self.assertIn('Fecha de envío: presente',s)
        self.assertIn('protección existente impide',s);self.assertNotIn('2026-11-11',s)
    async def test_missing_creds(self):
        s=await c.diagnostic('','');self.assertIn('Faltan credenciales',s);self.assertEqual(Session.calls,[])

if __name__=='__main__':unittest.main()
