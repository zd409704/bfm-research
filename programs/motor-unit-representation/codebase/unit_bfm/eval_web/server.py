"""Serve the local evaluation UI, serialized jobs, and saved trajectory APIs."""
import argparse
import json
import mimetypes
import os
from pathlib import Path
import signal
import subprocess
import sys
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from . import data
from .worker import write
from .live import Manager
from . import parameters

STATIC = Path(__file__).parent/'static'


class Jobs:
    def __init__(self):
        self.lock=threading.RLock()
        self.process=None
        self.path=None

    def status(self):
        with self.lock:
            if self.path is None:
                return None
            job=data.read_json(self.path,{})
            if self.process is not None and self.process.poll() is not None and job.get('status')=='running':
                job.update(status='failed',stage='Executing failed, see log',returncode=self.process.returncode,finished_at=time.time())
                write(self.path,job)
            log=self.path.parent/'output.log'
            if log.exists():
                with log.open('rb') as stream:
                    stream.seek(max(0,log.stat().st_size-18000))
                    job['log']=stream.read().decode('utf-8',errors='replace')
            return job

    def start(self, checkpoint, plan):
        with self.lock:
            if self.process is not None and self.process.poll() is None:
                raise ValueError('The evaluation is in progress, please wait for or stop the current evaluation')
            if checkpoint not in {r['id'] for r in data.checkpoints()}:
                raise ValueError('Please select the V2 checkpoint in the list')
            if plan not in {r['id'] for r in data.PLANS}:
                raise ValueError('Unknown assessment item')
            job_id=time.strftime('%Y%m%d_%H%M%S')+'_'+uuid.uuid4().hex[:6]
            folder=data.ARTIFACTS/'web_evaluations'/job_id
            folder.mkdir(parents=True,exist_ok=False)
            self.path=folder/'job.json'
            write(self.path,dict(id=job_id,checkpoint=checkpoint,plan=plan,status='running',
                created_at=time.time(),stage='Prepare to run.',results=[]))
            with (folder/'output.log').open('wb') as log:
                self.process=subprocess.Popen([sys.executable,'-u','-m','unit_bfm.eval_web.worker',
                    '--job',str(self.path)],cwd=data.ROOT,stdout=log,stderr=subprocess.STDOUT,
                    start_new_session=True,env={**os.environ,'PYTHONUNBUFFERED':'1'})
            return self.status()

    def cancel(self):
        with self.lock:
            if self.process is None or self.process.poll() is not None:
                raise ValueError('No assessment under implementation')
            os.killpg(self.process.pid,signal.SIGTERM)
            job=data.read_json(self.path,{})
            job.update(status='cancelled',stage='Stopped, partial result and log maintained',finished_at=time.time())
            write(self.path,job)
            return self.status()


JOBS=Jobs()
LIVE=Manager()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        if args and str(args[0]).startswith('POST'):
            super().log_message(fmt,*args)

    def json(self,payload,status=200):
        encoded=json.dumps(data.clean(payload),ensure_ascii=False,allow_nan=False).encode()
        self.send_response(status)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Content-Length',str(len(encoded)))
        self.send_header('Cache-Control','no-store')
        self.end_headers()
        self.wfile.write(encoded)

    def local_host(self):
        return self.headers.get('Host') in {f'127.0.0.1:{self.server.server_port}',f'localhost:{self.server.server_port}'}

    def send_file(self,path):
        size=path.stat().st_size
        start,end=0,size-1
        requested=self.headers.get('Range')
        if requested:
            import re
            match=re.fullmatch(r'bytes=(\d+)-(\d*)',requested)
            if not match:
                self.send_error(416);return
            start=int(match[1]);end=min(int(match[2]) if match[2] else size-1,size-1)
            if start>end or start>=size:
                self.send_error(416);return
        self.send_response(206 if requested else 200)
        self.send_header('Content-Type',mimetypes.guess_type(path.name)[0] or 'application/octet-stream')
        self.send_header('Content-Length',str(end-start+1))
        self.send_header('Accept-Ranges','bytes')
        self.send_header('X-Content-Type-Options','nosniff')
        if requested:self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
        if path.suffix in ('.npz','.xml'):
            self.send_header('Content-Disposition',f'attachment; filename="{path.name}"')
        self.end_headers()
        with path.open('rb') as stream:
            stream.seek(start);left=end-start+1
            while left:
                block=stream.read(min(65536,left))
                if not block:break
                self.wfile.write(block);left-=len(block)

    def do_GET(self):
        try:
            if not self.local_host():
                return self.json({'error':'Only accept local address'},403)
            parsed=urlparse(self.path)
            query={k:v[-1] for k,v in parse_qs(parsed.query).items()}
            path=parsed.path
            if path=='/api/live/parameters':
                return self.json(dict(groups=parameters.GROUPS,fields=parameters.FIELDS))
            if path=='/api/catalog':
                videos=[dict(label=p.stem,url='/asset?path='+p.relative_to(data.ARTIFACTS).as_posix())
                    for p in sorted((data.ARTIFACTS/'rf_v2_full/videos').glob('*.mp4'))]
                return self.json(dict(checkpoints=data.checkpoints(),plans=data.PLANS,
                    evaluations=data.evaluations(),videos=videos,job=JOBS.status()))
            if path=='/api/evaluation':return self.json(data.detail(query['id']))
            if path=='/api/cases':
                _,p,arrays=data.dataset(query['id'],query['file'])
                return self.json([data.case_metadata(arrays,i,p.name) for i in range(len(arrays['y']))])
            if path=='/api/trajectory':
                return self.json(data.trajectory(query['id'],query['file'],int(query['index'])))
            if path=='/api/job':return self.json(JOBS.status())
            if path=='/api/live/state':
                return self.json(LIVE.state(int(query.get('since',0)),query.get('id')))
            if path=='/asset':
                file=data.confined(data.ARTIFACTS,query['path'])
                if not file.is_file() or file.suffix not in ('.mp4','.png','.json','.npz','.xml'):
                    raise ValueError('This file cannot be downloaded')
                return self.send_file(file)
            static_name='index.html' if path=='/' else path.lstrip('/')
            if static_name not in ('index.html','app.js','style.css'):
                return self.json({'error':'Page does not exist'},404)
            return self.send_file(STATIC/static_name)
        except (ValueError,KeyError,FileNotFoundError) as exc:
            self.json({'error':str(exc)},400)
        except (BrokenPipeError,ConnectionResetError):
            pass
        except Exception as exc:
            import traceback
            traceback.print_exc()
            self.json({'error':str(exc)},500)

    def do_POST(self):
        try:
            origin=self.headers.get('Origin')
            if not self.local_host() or (origin and origin not in {f'http://127.0.0.1:{self.server.server_port}',f'http://localhost:{self.server.server_port}'}):
                return self.json({'error':'Accept only co-source operations'},403)
            if self.headers.get('Content-Type','').split(';')[0]!='application/json':
                return self.json({'error':'Request must use JSON'},415)
            length=int(self.headers.get('Content-Length','0'))
            if length<0 or length>4096:raise ValueError('It\'s too much.')
            payload=json.loads(self.rfile.read(length) or b'{}')
            if self.path=='/api/run':return self.json(JOBS.start(payload['checkpoint'],payload['plan']),202)
            if self.path=='/api/cancel':return self.json(JOBS.cancel())
            if self.path=='/api/live/sample':
                seed=float(payload.get('seed',20261001));role=float(payload.get('role',0))
                if not 0<=seed<=2**32-1 or seed!=int(seed) or role not in (0,1,2,3):
                    raise ValueError('Invalid random torrent or character')
                return self.json(parameters.sample(int(seed),int(role)))
            if self.path=='/api/live/start':return self.json(LIVE.start(payload))
            if self.path=='/api/live/pulse':
                return self.json(LIVE.current(payload.get('id')).inject(payload))
            if self.path=='/api/live/control':
                exp=LIVE.current(payload.get('id'))
                exp.control(payload['action'])
                if payload['action']=='stop' and exp.thread:
                    exp.thread.join(timeout=10)
                return self.json(dict(id=exp.meta['id'],status=exp.status))
            return self.json({'error':'Operation does not exist'},404)
        except (ValueError,KeyError) as exc:
            self.json({'error':str(exc)},400)
        except Exception as exc:
            import traceback
            traceback.print_exc()
            self.json({'error':str(exc)},500)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--port',type=int,default=8766)
    args=parser.parse_args()
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    print(f'Assessment web site: http://127.0.0.1{server.server_port}',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()


if __name__=='__main__':main()
