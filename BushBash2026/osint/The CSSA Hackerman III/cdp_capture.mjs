import fs from 'node:fs';

const port = process.argv[2] || '9223';
const output = process.argv[3] || 'cdp.png';
const pages = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
const page = pages.find(x => x.type === 'page' && x.url.includes('google.com/maps'));
if (!page) throw new Error('Google Maps page not found');
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((resolve, reject) => { ws.onopen = resolve; ws.onerror = reject; });
let seq = 0;
function call(method, params={}) {
  const id = ++seq;
  ws.send(JSON.stringify({id, method, params}));
  return new Promise((resolve, reject) => {
    const handler = e => {
      const msg = JSON.parse(e.data);
      if (msg.id !== id) return;
      ws.removeEventListener('message', handler);
      msg.error ? reject(new Error(JSON.stringify(msg.error))) : resolve(msg.result);
    };
    ws.addEventListener('message', handler);
  });
}
await call('Page.bringToFront');
await new Promise(r => setTimeout(r, 4000));
const shot = await call('Page.captureScreenshot', {format:'png', fromSurface:true, captureBeyondViewport:false});
fs.writeFileSync(output, Buffer.from(shot.data, 'base64'));
console.log(JSON.stringify({title: page.title, url: page.url, output}));
ws.close();
