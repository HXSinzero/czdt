const normalizeBasePath = (value) => {
  if (!value) return '/'
  const withLeadingSlash = value.startsWith('/') ? value : `/${value}`
  return withLeadingSlash.endsWith('/') ? withLeadingSlash : `${withLeadingSlash}/`
}

const normalizeApiBaseUrl = (value) => {
  if (!value) return '/api'
  return value.endsWith('/') ? value.slice(0, -1) : value
}

export const appConfig = {
  basePath: normalizeBasePath(import.meta.env.VITE_BASE_PATH),
  apiBaseUrl: normalizeApiBaseUrl(import.meta.env.VITE_API_BASE_URL)
}
