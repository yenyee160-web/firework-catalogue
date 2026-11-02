<script setup>
import { computed, onMounted, ref, watch } from 'vue'
const products = ref([])
const loading = ref(true)
const error = ref('')
const query = ref('')
const category = ref('All')
const cart = ref({})
const checkoutError = ref('')
const money = cents => 'RM ' + (cents / 100).toFixed(2)
const categories = computed(() => ['All', ...new Set(products.value.map(p => p.category))])
const filtered = computed(() => products.value.filter(p =>
  (category.value === 'All' || p.category === category.value) &&
  (p.name + ' ' + p.description).toLowerCase().includes(query.value.toLowerCase())))
const cartLines = computed(() => products.value.filter(p => cart.value[p.id] > 0).map(p => ({ ...p, quantity: cart.value[p.id] })))
const count = computed(() => cartLines.value.reduce((n, p) => n + p.quantity, 0))
const total = computed(() => cartLines.value.reduce((n, p) => n + p.price_sen * p.quantity, 0))
function change(id, delta) {
  const current = Number(cart.value[id]) || 0
  const next = Math.max(0, Math.min(25, current + delta))
  cart.value = { ...cart.value, [id]: next }
}
watch(cart, value => localStorage.setItem('fireworks-cart-v1', JSON.stringify(value)), { deep: true })
onMounted(async () => {
  try {
    const saved = JSON.parse(localStorage.getItem('fireworks-cart-v1') || '{}')
    if (saved && typeof saved === 'object' && !Array.isArray(saved)) {
      cart.value = Object.fromEntries(Object.entries(saved).filter(([id, quantity]) => typeof id === 'string' && Number.isInteger(quantity) && quantity > 0 && quantity <= 25))
    }
  } catch { cart.value = {} }
  try {
    const response = await fetch('/api/products/')
    if (!response.ok) throw new Error('Cannot load products')
    const data = await response.json()
    products.value = data.products
    const allowed = new Set(data.products.filter(p => p.available).map(p => p.id))
    cart.value = Object.fromEntries(Object.entries(cart.value).filter(([id]) => allowed.has(id)))
  } catch (e) { error.value = e.message } finally { loading.value = false }
})
async function checkout() {
  checkoutError.value = ''
  try {
    const response = await fetch('/api/enquiry/', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ items: cartLines.value.map(p => ({ id: p.id, quantity: p.quantity })) })
    })
    const data = await response.json()
    if (!response.ok) throw new Error(data.error || 'Unable to prepare enquiry')
    // Customer chooses whether to send; tests never click the outgoing WhatsApp URL.
    window.open(data.url, '_blank', 'noopener,noreferrer')
  } catch (e) { checkoutError.value = e.message }
}
</script>

<template>
  <div class="page">
    <header class="topbar"><a class="brand" href="/">✦ Celebration Catalogue</a><span>Browse · Enquire · Confirm</span></header>
    <section class="hero"><span class="eyebrow">FESTIVE COLLECTION</span><h1>Make every moment sparkle.</h1>
      <p>Explore our sample celebration catalogue. Select products and send a WhatsApp enquiry—no online payment or completed order.</p>
      <a href="#catalogue" class="pill">Explore collection ↓</a>
    </section>
    <main id="catalogue" class="layout">
      <section class="catalogue"><div class="section-head"><div><span class="eyebrow">THE COLLECTION</span><h2>Find your celebration</h2></div><span>{{ filtered.length }} products</span></div>
        <label class="search-label">Search products<input v-model="query" aria-label="Search products" placeholder="Search by name or description…" /></label>
        <div class="filters"><button v-for="item in categories" :key="item" :class="{ active: category === item }" @click="category = item">{{ item }}</button></div>
        <p v-if="loading" role="status">Loading catalogue…</p><p v-if="error" role="alert">{{ error }}</p>
        <div class="cards">
          <article v-for="product in filtered" :key="product.id" class="product-card" data-testid="product-card">
            <div class="product-art"><span>{{ product.icon || '✨' }}</span></div>
            <div class="product-info"><small>{{ product.category }}</small><h3>{{ product.name }}</h3><p>{{ product.description }}</p>
              <div class="product-bottom"><strong>{{ money(product.price_sen) }}</strong><button :data-testid="'add-' + product.id" :disabled="!product.available" @click="change(product.id, 1)">{{ product.available ? 'Add +' : 'Unavailable' }}</button></div>
            </div>
          </article>
        </div><p v-if="!loading && !error && !filtered.length">No products match your search.</p>
      </section>
      <aside class="cart"><div class="cart-heading"><h2>Your enquiry</h2><span data-testid="cart-count">{{ count }}</span></div><p class="cart-note">Your selection is saved in this browser.</p>
        <p v-if="!cartLines.length" class="empty">Your basket is empty. Add an item to begin.</p>
        <div v-for="item in cartLines" :key="item.id" class="cart-line"><div><strong>{{ item.name }}</strong><small>{{ money(item.price_sen) }} each</small></div>
          <div class="quantity"><button :aria-label="'Decrease ' + item.name + ' quantity'" @click="change(item.id, -1)">−</button><span :data-testid="'quantity-' + item.id">{{ item.quantity }}</span><button :aria-label="'Increase ' + item.name + ' quantity'" @click="change(item.id, 1)">+</button></div></div>
        <div class="subtotal"><span>Estimated total</span><strong data-testid="cart-total">{{ money(total) }}</strong></div>
        <button class="checkout" :disabled="!cartLines.length" @click="checkout">Prepare WhatsApp enquiry ↗</button>
        <p v-if="checkoutError" role="alert">{{ checkoutError }}</p>
        <p class="disclaimer">Enquiry only. No order is placed or payment collected. Confirm availability and local eligibility with the business.</p>
      </aside>
    </main><footer>Fictional demonstration products · Replace before publishing · Follow applicable local regulations.</footer>
  </div>
</template>
