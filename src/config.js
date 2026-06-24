const normalizeBasePath = (value) => {
  if (!value) return '/'
  const withLeadingSlash = value.startsWith('/') ? value : `/${value}`
  return withLeadingSlash.endsWith('/') ? withLeadingSlash : `${withLeadingSlash}/`
}

const normalizeApiBaseUrl = (value) => {
  if (!value) return '/api'
  return value.endsWith('/') ? value.slice(0, -1) : value
}

const absolutePattern = /^(?:[a-z][a-z\d+.-]*:)?\/\//i
const specialUrlPattern = /^(?:data|blob):/i

function normalizePublicPath(path, baseDir = '') {
  const value = String(path || '').trim()
  if (!value || absolutePattern.test(value) || specialUrlPattern.test(value)) return value

  const base = normalizeBasePath(import.meta.env.BASE_URL || import.meta.env.VITE_BASE_PATH)

  if (value.startsWith('/')) {
    return `${base}${value.replace(/^\/+/, '')}`
  }

  const normalizedBaseDir = String(baseDir || '').replace(/^\/+|\/+$/g, '')
  const source = value.startsWith('./') || value.startsWith('../')
    ? `${normalizedBaseDir}/${value}`
    : value

  const parts = []
  source.split('/').forEach((part) => {
    if (!part || part === '.') return
    if (part === '..') {
      parts.pop()
      return
    }
    parts.push(part)
  })

  return `${base}${parts.join('/')}`
}

export const appConfig = {
  basePath: normalizeBasePath(import.meta.env.BASE_URL || import.meta.env.VITE_BASE_PATH),
  apiBaseUrl: normalizeApiBaseUrl(import.meta.env.VITE_API_BASE_URL)
}

export function getPublicAssetUrl(path, baseDir = '') {
  return normalizePublicPath(path, baseDir)
}
