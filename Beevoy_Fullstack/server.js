'use strict';
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const {URL} = require('node:url');
const PORT = Number(process.env.PORT) || 3000;
const ROOT = path.resolve(__dirname, 'public');
const catalog = [
  {id:'everyday', name:'Mānuka Honey — Everyday', grade:'MGO 100+*', size:'250 g', priceINR:2499, priceNZD:49, category:'everyday', tag:'Everyday favourite', description:'A gentle introduction to the distinctive character of Mānuka honey.'},
  {id:'signature', name:'Mānuka Honey — Signature', grade:'MGO 250+*', size:'250 g', priceINR:4499, priceNZD:89, category:'signature', tag:'Popular choice', description:'An expressive golden honey for memorable everyday rituals.'},
  {id:'reserve', name:'Mānuka Honey — Reserve', grade:'MGO 550+*', size:'250 g', priceINR:7999, priceNZD:159, category:'reserve', tag:'Premium collection', description:'An elevated selection for honey lovers and thoughtful gifting.'},
  {id:'gift', name:'Beevoy Discovery Gift Set', grade:'GIFT COLLECTION', size:'2 × 125 g', priceINR:5999, priceNZD:119, category:'gifts', tag:'Gift-ready', description:'A beautiful introduction to two distinctive honey experiences.'}
];
const mime = {'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp','.ico':'image/x-icon'};
function json(res,status,payload){const body=JSON.stringify(payload);res.writeHead(status,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store','Content-Length':Buffer.byteLength(body)});res.end(body)}
function readJson(req){return new Promise((resolve,reject)=>{let data='';req.on('data',chunk=>{data+=chunk;if(data.length>16000){reject(new Error('Request too large'));req.destroy()}});req.on('end',()=>{try{resolve(JSON.parse(data||'{}'))}catch{reject(new Error('Invalid JSON'))}});req.on('error',reject)})}
const server=http.createServer(async(req,res)=>{
  const url=new URL(req.url,'http://localhost');
  if(url.pathname==='/api/health'&&req.method==='GET')return json(res,200,{ok:true,project:'Beevoy demo',time:new Date().toISOString()});
  if(url.pathname==='/api/products'&&req.method==='GET')return json(res,200,{products:catalog,notice:'Sample catalog: prices, grades and product availability are illustrative only.'});
  if(url.pathname==='/api/newsletter'&&req.method==='POST'){
    try{const body=await readJson(req);if(typeof body.email!=='string'||!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(body.email)||body.email.length>254)return json(res,400,{error:'Enter a valid email address.'});return json(res,200,{ok:true,message:'Demo request received. Email was not stored or subscribed.'})}catch(err){return json(res,400,{error:err.message})}
  }
  if(url.pathname==='/api/checkout'&&req.method==='POST'){
    try{const body=await readJson(req);const market=body.market==='NZ'?'NZ':'IN';if(!Array.isArray(body.items)||!body.items.length)return json(res,400,{error:'Your bag is empty.'});let total=0;for(const item of body.items){const product=catalog.find(p=>p.id===item.id);if(!product||!Number.isInteger(item.quantity)||item.quantity<1||item.quantity>20)return json(res,400,{error:'Invalid cart contents.'});total+=(market==='NZ'?product.priceNZD:product.priceINR)*item.quantity}return json(res,200,{ok:true,demo:true,market,total,currency:market==='NZ'?'NZD':'INR',message:'Demo checkout summary only. No order was placed and no payment was taken.'})}catch(err){return json(res,400,{error:err.message})}
  }
  if(url.pathname.startsWith('/api/'))return json(res,404,{error:'Endpoint not found.'});
  if(req.method!=='GET'&&req.method!=='HEAD')return json(res,405,{error:'Method not allowed.'});
  let requested;
  try{requested=decodeURIComponent(url.pathname)}catch{return json(res,400,{error:'Invalid URL'})}
  const target=path.resolve(ROOT,'.'+(requested==='/'?'/index.html':requested));
  if(target!==ROOT&&!target.startsWith(ROOT+path.sep)){res.writeHead(403);return res.end('Forbidden')}
  fs.stat(target,(err,stats)=>{
    if(err||!stats.isFile()){res.writeHead(404,{'Content-Type':'text/plain; charset=utf-8'});return res.end('404 Not found')}
    res.writeHead(200,{'Content-Type':mime[path.extname(target)]||'application/octet-stream','X-Content-Type-Options':'nosniff'});
    if(req.method==='HEAD')return res.end();
    fs.createReadStream(target).pipe(res);
  });
});
server.listen(PORT,()=>console.log(`Beevoy running at http://localhost:${PORT}`));
