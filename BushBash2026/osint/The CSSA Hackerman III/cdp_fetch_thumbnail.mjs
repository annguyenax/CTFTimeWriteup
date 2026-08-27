import fs from 'node:fs';
const port=process.argv[2]||'9223', output=process.argv[3]||'thumb.jpg';
const pages=await(await fetch(`http://127.0.0.1:${port}/json`)).json();
const page=pages.find(x=>x.type==='page'&&x.url.includes('google.com/maps'));
if(!page)throw new Error('Maps page not found');
const ws=new WebSocket(page.webSocketDebuggerUrl);await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j});
let n=0;function call(method,params={}){const id=++n;ws.send(JSON.stringify({id,method,params}));return new Promise((r,j)=>{const h=e=>{const m=JSON.parse(e.data);if(m.id!==id)return;ws.removeEventListener('message',h);m.error?j(new Error(JSON.stringify(m.error))):r(m.result)};ws.addEventListener('message',h)})}
const m=decodeURIComponent(page.url).match(/https:\/\/streetviewpixels-pa\.googleapis\.com\/v1\/thumbnail[^!]+/);
if(!m)throw new Error('embedded thumbnail URL not found');
const expression=`(async()=>{const r=await fetch(${JSON.stringify(m[0])});const b=await r.blob();return {status:r.status,type:b.type,data:await new Promise(ok=>{const f=new FileReader();f.onload=()=>ok(f.result);f.readAsDataURL(b)})}})()`;
const result=await call('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});
const v=result.result.value;console.log(JSON.stringify({url:m[0],status:v?.status,type:v?.type}));
if(v?.data?.includes(','))fs.writeFileSync(output,Buffer.from(v.data.split(',')[1],'base64'));
ws.close();
