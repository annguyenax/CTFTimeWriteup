import fs from 'node:fs';import path from 'node:path';
const input=process.argv[2],outdir=process.argv[3],port=process.argv[4]||'9223';
fs.mkdirSync(outdir,{recursive:true});const recs=JSON.parse(fs.readFileSync(input,'utf8'));
const pages=await(await fetch(`http://127.0.0.1:${port}/json`)).json();const page=pages.find(x=>x.type==='page'&&x.url.includes('google.com/maps'));
if(!page)throw new Error('Maps page missing');const ws=new WebSocket(page.webSocketDebuggerUrl);await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j});
let n=0;function call(method,params={}){const id=++n;ws.send(JSON.stringify({id,method,params}));return new Promise((r,j)=>{const h=e=>{const m=JSON.parse(e.data);if(m.id!==id)return;ws.removeEventListener('message',h);m.error?j(new Error(JSON.stringify(m.error))):r(m.result)};ws.addEventListener('message',h)})}
for(let i=0;i<recs.length;i++){
 const r=recs[i],url=`https://streetviewpixels-pa.googleapis.com/v1/thumbnail?cb_client=maps_sv.tactile&w=900&h=600&pitch=0&panoid=${encodeURIComponent(r.panoid)}&yaw=${r.yaw}&thumbfov=78`;
 const expr=`(async()=>{const r=await fetch(${JSON.stringify(url)});const b=await r.blob();return {s:r.status,t:b.type,d:await new Promise(ok=>{const f=new FileReader();f.onload=()=>ok(f.result);f.readAsDataURL(b)})}})()`;
 const z=(await call('Runtime.evaluate',{expression:expr,awaitPromise:true,returnByValue:true})).result.value;
 if(z?.s===200&&z.d?.includes(',')){const fn=`${String(i).padStart(4,'0')}_${r.suburb}_${r.street}_${Math.round(r.yaw)}.jpg`.replaceAll("'",'').replaceAll(' ','_');fs.writeFileSync(path.join(outdir,fn),Buffer.from(z.d.split(',')[1],'base64'));r.file=fn;}
 else console.log('skip',i,z?.s,z?.t);
}
fs.writeFileSync(path.join(outdir,'metadata.json'),JSON.stringify(recs,null,2));console.log('done',recs.filter(x=>x.file).length);ws.close();
