const port = process.argv[2] || '9223';
const needle = process.argv[3] || 'bushbash.cssa.club';
const pages = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
const page = pages.find(x => x.type === 'page' && x.url.includes(needle));
if (!page) throw new Error(`Page not found: ${needle}`);
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((resolve, reject) => { ws.onopen = resolve; ws.onerror = reject; });
let seq = 0;
function call(method, params = {}) {
  const id = ++seq;
  ws.send(JSON.stringify({id, method, params}));
  return new Promise((resolve, reject) => {
    const handler = event => {
      const msg = JSON.parse(event.data);
      if (msg.id !== id) return;
      ws.removeEventListener('message', handler);
      msg.error ? reject(new Error(JSON.stringify(msg.error))) : resolve(msg.result);
    };
    ws.addEventListener('message', handler);
  });
}
await new Promise(r => setTimeout(r, 5000));
const expression = `JSON.stringify({url:location.href,title:document.title,text:document.body?.innerText,html:document.documentElement?.outerHTML})`;
const result = await call('Runtime.evaluate', {expression, returnByValue: true});
console.log(result.result.value);
ws.close();
