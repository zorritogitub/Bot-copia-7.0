"""In-process mocks; no network requests to any server."""
import asyncio
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import aiohttp
import varela_client as c

class Response:
    def __init__(self,status=200,text='',data=None, wait=None):
        self.status=status;self.body=text;self.data=data;self.wait=wait
    async def __aenter__(self):
        if self.wait: await self.wait.wait()
        return self
    async def __aexit__(self,*args): pass
    async def text(self): return self.body
    async def json(self,**kw):
        if self.data is None: raise ValueError('bad json')
        return self.data

class Session:
    variant='ok'; calls=[]; started=None; hold=None
    def __init__(self,*a,**kw): pass
    async def __aenter__(self): return self
    async def __aexit__(self,*a): pass
    def get(self,url,**kw):
        if url.endswith('/login'):
            self.calls.append('login')
            captcha='<div class="g-recaptcha"></div>' if self.variant=='captcha' else ''
            return Response(text='<input name="csrfToken" value="cs">'+captcha)
        if url.endswith('/submission'):
            self.calls.append('page')
            if self.variant in ('rejected','captcha_rejected'): return Response(status=302)
            return Response(text='pkp.currentUser = {"csrfToken":"auth","id":7};')
        self.calls.append('draft')
        return Response(data={'id':2164,'submissionProgress': '' if self.variant=='submitted' else 'files', 'dateSubmitted':'2026-11-11' if self.variant=='ambiguous' else None})
    def post(self,url,**kw):
        if url.endswith('/login/signIn'):
            self.calls.append('sign')
            if self.variant=='captcha_rejected': return Response(status=200,text='<div>Error: captcha incorrecto</div>')
            return Response(status=302)
        self.calls.append('upload')
        assert kw['headers']['X-Csrf-Token']=='auth'
        form=kw['data']; fields=form._fields
        assert [f[0]['name'] for f in fields]==['fileStage','file']
        assert fields[0][2]=='2' and fields[1][0]['filename']=='test.txt'
        assert fields[1][2].read()==b'mock file\n'
        # Force actual multipart serialization; seek back after inspecting.
        fields[1][2].seek(0); assert form().content_type.startswith('multipart/form-data;')
        self.started.set()
        if self.variant in ('cancel','timeout'): return Response(wait=self.hold)
        if self.variant=='http_error': return Response(status=400,data={'id':9})
        if self.variant=='bad_json': return Response()
        if self.variant=='wrong_id': return Response(data={'id':9,'submissionId':44,'fileStage':2,'uploaderUserId':7})
        return Response(data={'id':9,'submissionId':2164,'fileStage':2,'uploaderUserId':7})

class Tests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.file=Path(self.tmp.name)/'test.txt';self.file.write_bytes(b'mock file\n')
        Session.variant='ok';Session.calls=[];Session.started=asyncio.Event();Session.hold=asyncio.Event()
        self.patch=patch.object(c.aiohttp,'ClientSession',Session);self.patch.start()
    async def asyncTearDown(self): self.patch.stop();self.tmp.cleanup()
    async def upload(self): return await c.upload(self.file,'user','password')
    async def test_success_multipart(self):
        self.assertEqual(await self.upload(),9); self.assertEqual(Session.calls,['login','sign','page','draft','upload'])
    async def test_captcha_markup_does_not_prove_rejection(self):
        Session.variant='captcha'
        self.assertEqual(await self.upload(),9)
        self.assertEqual(Session.calls,['login','sign','page','draft','upload'])
    async def test_captcha_rejected_once(self):
        Session.variant='captcha_rejected'
        with self.assertRaisesRegex(c.VarelaError,'CAPTCHA'): await self.upload()
        self.assertEqual(Session.calls,['login','sign','page'])
    async def test_rejected_once(self):
        Session.variant='rejected'
        with self.assertRaises(c.VarelaError): await self.upload()
        self.assertEqual(Session.calls,['login','sign','page'])
    async def test_submitted(self):
        Session.variant='submitted'
        with self.assertRaises(c.VarelaError): await self.upload()
        self.assertNotIn('upload',Session.calls)
    async def test_ambiguous_submitted_date(self):
        Session.variant='ambiguous'
        with self.assertRaisesRegex(c.VarelaError,'fecha de envío'): await self.upload()
        self.assertNotIn('upload',Session.calls)
    async def test_no_false_success(self):
        for variant in ('http_error','bad_json','wrong_id'):
            Session.variant=variant
            with self.assertRaises(c.VarelaError): await self.upload()
    async def test_cancel(self):
        Session.variant='cancel';t=asyncio.create_task(self.upload());await Session.started.wait();t.cancel()
        with self.assertRaises(asyncio.CancelledError): await t
    async def test_timeout(self):
        Session.variant='timeout'
        with self.assertRaises(asyncio.TimeoutError): await asyncio.wait_for(self.upload(),.05)
    async def test_missing_credentials(self):
        with self.assertRaises(c.VarelaError): await c.upload(self.file,'','')
        self.assertEqual(Session.calls,[])

if __name__=='__main__': unittest.main()
