const REF_KEY = 'guanlian_ref'
const REF_TS_KEY = 'guanlian_ref_ts'
const BIND_DAYS = 7

export function captureReferral(code) {
  if (!code || typeof code !== 'string') return
  localStorage.setItem(REF_KEY, code.trim())
  localStorage.setItem(REF_TS_KEY, String(Date.now()))
}

export function getReferralCode() {
  const code = localStorage.getItem(REF_KEY)
  const ts = Number(localStorage.getItem(REF_TS_KEY) || 0)
  if (!code) return ''
  if (Date.now() - ts > BIND_DAYS * 24 * 60 * 60 * 1000) {
    clearReferral()
    return ''
  }
  return code
}

export function clearReferral() {
  localStorage.removeItem(REF_KEY)
  localStorage.removeItem(REF_TS_KEY)
}

export function fullUrl(path) {
  if (typeof window === 'undefined') return path
  if (path.startsWith('http')) return path
  return `${window.location.origin}${path.startsWith('/') ? path : `/${path}`}`
}

export function qrCodeUrl(text) {
  return `https://api.qrserver.com/v1/create-qr-code/?size=140x140&data=${encodeURIComponent(text)}`
}
