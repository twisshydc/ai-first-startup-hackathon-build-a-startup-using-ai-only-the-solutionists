'use strict';
const $ = (selector) => document.querySelector(selector);
const elements = {
  market: $('#market'), category: $('#category'), products: $('#product-grid'), cartCount: $('#cart-count'), drawerCount: $('#drawer-count'),
  drawer: $('#cart-drawer'), scrim: $('#scrim'), cartItems: $('#cart-items'), subtotal: $('#subtotal'),
  modal: $('#product-modal'), modalTitle: $('#modal-title'), modalDescription: $('#modal-description'), modalGrade: $('#modal-grade'),
  modalSize: $('#modal-size'), modalPrice: $('#modal-price'), qty: $('#qty-value'), toast: $('#toast')
};
let products = [];
let market = localStorage.getItem('beevoy_market') === 'NZ' ? 'NZ' : 'IN';
let cart = [];
try { const saved = JSON.parse(localStorage.getItem('beevoy_cart') || '[]'); if(Array.isArray(saved)) cart = saved.filter(x => x && typeof x.id === 'string' && Number.isInteger(x.quantity) && x.quantity > 0 && x.quantity <= 20); } catch { cart = []; }
let activeProduct = null;
let selectedQty = 1;
let toastTimer;
const money = (amount) => new Intl.NumberFormat(market === 'NZ' ? 'en-NZ' : 'en-IN', {style:'currency',currency:market === 'NZ' ? 'NZD' : 'INR',maximumFractionDigits:0}).format(amount);
const price = p => market === 'NZ' ? p.priceNZD : p.priceINR;
function saveCart(){ localStorage.setItem('beevoy_cart', JSON.stringify(cart)); }
function notice(message){ elements.toast.textContent = message; elements.toast.classList.add('show'); clearTimeout(toastTimer); toastTimer = setTimeout(() => elements.toast.classList.remove('show'), 3200); }
function miniJar(p){ return `<div class="mini-jar" aria-hidden="true"><div class="mini-lid"></div><div class="mini-body"><span>✺</span><strong>Beevoy</strong><small>MĀNUKA HONEY</small><b>${p.grade.replace('*','')}</b></div></div>`; }
function renderProducts(){
  const category = elements.category.value;
  const shown = products.filter(p=> category === 'all' || p.category === category);
  elements.products.innerHTML = shown.length ? shown.map(p => `<article class="product-card"><div class="product-visual"><span class="product-tag">${p.tag}</span>${miniJar(p)}</div><div class="product-details"><small>${p.grade} · ${p.size}</small><h3>${p.name}</h3><p>${p.description}</p><div class="product-purchase"><strong>${money(price(p))}</strong><button type="button" data-add="${p.id}" aria-label="Add ${p.name} to bag">+</button></div><button class="product-open" type="button" data-view="${p.id}">View product details →</button></div></article>`).join('') : '<p>No products in this category.</p>';
}
function renderCart(){
  cart = cart.filter(item => products.some(p=>p.id === item.id)); saveCart();
  const count = cart.reduce((sum,item)=>sum+item.quantity,0);
  elements.cartCount.textContent = count; elements.drawerCount.textContent = `(${count})`;
  if(!cart.length) elements.cartItems.innerHTML = `<div class="empty-bag"><div style="font-size:55px;color:#bb933c">♧</div><h3>Your bag is empty</h3><p>Beautiful honey is just a click away.</p></div>`;
  else elements.cartItems.innerHTML = cart.map(item => {const p = products.find(x=>x.id===item.id);return `<div class="cart-item"><div class="cart-thumb">✺</div><div><h3>${p.name}</h3><small>${p.size} · ${p.grade}</small><div class="cart-qty"><button data-cart-change="${p.id}" data-delta="-1" aria-label="Decrease ${p.name}">−</button><span>${item.quantity}</span><button data-cart-change="${p.id}" data-delta="1" aria-label="Increase ${p.name}">+</button><button class="remove-btn" data-remove="${p.id}">Remove</button></div></div><strong>${money(price(p)*item.quantity)}</strong></div>`}).join('');
  elements.subtotal.textContent = money(cart.reduce((sum,item)=>sum+price(products.find(p=>p.id === item.id))*item.quantity,0));
  $('#checkout').disabled = !cart.length;
}
function addToCart(id,quantity=1){ const p = products.find(x=>x.id===id); if(!p)return; const item=cart.find(x=>x.id===id); if(item)item.quantity=Math.min(20,item.quantity+quantity); else cart.push({id,quantity}); renderCart(); notice(`${p.name} added to your bag.`); }
function changeCart(id,delta){ const item=cart.find(x=>x.id===id); if(!item)return; item.quantity+=delta; if(item.quantity<=0)cart=cart.filter(x=>x.id!==id);else item.quantity=Math.min(20,item.quantity);renderCart(); }
function showScrim(){elements.scrim.hidden=false;document.body.style.overflow='hidden'}
function hideScrim(){if(elements.drawer.classList.contains('open') || elements.modal.classList.contains('open'))return;elements.scrim.hidden=true;document.body.style.overflow=''}
function openCart(){closeModal();elements.drawer.classList.add('open');elements.drawer.setAttribute('aria-hidden','false');showScrim();$('#cart-close').focus()}
function closeCart(){elements.drawer.classList.remove('open');elements.drawer.setAttribute('aria-hidden','true');hideScrim()}
function openModal(id){const p=products.find(x=>x.id===id);if(!p)return;closeCart();activeProduct=p;selectedQty=1;elements.qty.textContent='1';elements.modalTitle.textContent=p.name;elements.modalDescription.textContent=p.description;elements.modalGrade.textContent=p.grade;elements.modalSize.textContent=p.size;elements.modalPrice.textContent=money(price(p));elements.modal.classList.add('open');elements.modal.setAttribute('aria-hidden','false');showScrim();$('#modal-close').focus()}
function closeModal(){elements.modal.classList.remove('open');elements.modal.setAttribute('aria-hidden','true');hideScrim()}
function setMarket(next){market=next==='NZ'?'NZ':'IN';elements.market.value=market;localStorage.setItem('beevoy_market',market);renderProducts();renderCart();if(activeProduct)elements.modalPrice.textContent=money(price(activeProduct));notice(market==='IN'?'Showing illustrative India prices.':'Showing illustrative New Zealand prices.');}
async function initialize(){try{const res=await fetch('/api/products');if(!res.ok)throw new Error('Unable to retrieve catalogue');const data=await res.json();products=data.products;elements.market.value=market;renderProducts();renderCart()}catch{elements.products.innerHTML='<p>Could not load products. Please confirm that the Node server is running.</p>';notice('Unable to load catalogue. Check your server.')}}
elements.products.addEventListener('click',e=>{const add=e.target.closest('[data-add]');const view=e.target.closest('[data-view]');if(add)addToCart(add.dataset.add);if(view)openModal(view.dataset.view)});
elements.cartItems.addEventListener('click',e=>{const change=e.target.closest('[data-cart-change]');const remove=e.target.closest('[data-remove]');if(change)changeCart(change.dataset.cartChange,Number(change.dataset.delta));if(remove){cart=cart.filter(x=>x.id!==remove.dataset.remove);renderCart()}});
elements.market.addEventListener('change',e=>setMarket(e.target.value)); elements.category.addEventListener('change',renderProducts);
$('#cart-open').addEventListener('click',openCart);$('#cart-close').addEventListener('click',closeCart);$('#modal-close').addEventListener('click',closeModal);elements.scrim.addEventListener('click',()=>{closeCart();closeModal()});
$('#qty-minus').addEventListener('click',()=>{selectedQty=Math.max(1,selectedQty-1);elements.qty.textContent=selectedQty});
$('#qty-plus').addEventListener('click',()=>{selectedQty=Math.min(20,selectedQty+1);elements.qty.textContent=selectedQty});
$('#modal-add').addEventListener('click',()=>{if(activeProduct){addToCart(activeProduct.id,selectedQty);closeModal();openCart()}});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeCart();closeModal()}});
$('#menu-toggle').addEventListener('click',()=>{const nav=$('#main-nav');const opened=nav.classList.toggle('open');$('#menu-toggle').setAttribute('aria-expanded',String(opened))});
$('#main-nav').addEventListener('click',e=>{if(e.target.closest('a')){$('#main-nav').classList.remove('open');$('#menu-toggle').setAttribute('aria-expanded','false')}});
document.querySelectorAll('[data-market]').forEach(btn=>btn.addEventListener('click',()=>{setMarket(btn.dataset.market);window.location.hash='#shop'}));
$('#newsletter-form').addEventListener('submit',async e=>{e.preventDefault();const form=e.currentTarget;const button=form.querySelector('button');button.disabled=true;try{const res=await fetch('/api/newsletter',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:$('#email').value.trim()})});const result=await res.json();if(!res.ok)throw new Error(result.error||'Request failed');form.reset();notice('Demo form submitted. No email was saved or subscribed.')}catch(err){notice(err.message)}finally{button.disabled=false}});
$('#checkout').addEventListener('click',async()=>{if(!cart.length)return;const button=$('#checkout');button.disabled=true;try{const res=await fetch('/api/checkout',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({market,items:cart})});const result=await res.json();if(!res.ok)throw new Error(result.error||'Could not review bag');notice(`Demo total: ${money(result.total)}. No payment taken and no order created.`)}catch(err){notice(err.message)}finally{button.disabled=false}});
initialize();
