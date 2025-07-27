import { useState, useEffect, useCallback } from 'react'
import axios from 'axios'

export interface Product {
  id: string
  title: string
  description: string
  price: number
  compare_price: number
  score: number
  category: string
  tags: string[]
  source_store: string
  facebook_ads: any[]
  tiktok_mentions: any[]
  trend_data: any
  supplier_links?: any
  supplier_prices?: any
  created_at?: string
  updated_at?: string
}

export type SortOption = 'score' | 'price' | 'price_high' | 'trend' | 'newest' | 'name'

export interface FilterOptions {
  searchTerm: string
  category: string
  minScore: number
  maxPrice: number
  tags: string[]
  store: string
}

export interface UseProductsReturn {
  products: Product[]
  loading: boolean
  error: string | null
  filteredProducts: Product[]
  filterOptions: FilterOptions
  sortBy: SortOption
  viewMode: 'grid' | 'list'
  savedProducts: string[]
  stats: {
    totalProducts: number
    highScoreProducts: number
    averageScore: string
    averagePrice: string
    totalFacebookAds: number
    totalTikTokMentions: number
  }
  setFilterOptions: (options: Partial<FilterOptions>) => void
  setSortBy: (sort: SortOption) => void
  setViewMode: (mode: 'grid' | 'list') => void
  toggleSavedProduct: (productId: string) => void
  refreshProducts: () => Promise<void>
  clearFilters: () => void
}

export function useProducts(): UseProductsReturn {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [filterOptions, setFilterOptions] = useState<FilterOptions>({
    searchTerm: '',
    category: 'all',
    minScore: 0,
    maxPrice: 1000,
    tags: [],
    store: 'all'
  })
  const [sortBy, setSortBy] = useState<SortOption>('score')
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [savedProducts, setSavedProducts] = useState<string[]>([])

  const fetchProducts = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      
      // Build query parameters
      const params = new URLSearchParams()
      if (filterOptions.searchTerm) params.append('search', filterOptions.searchTerm)
      if (filterOptions.category !== 'all') params.append('category', filterOptions.category)
      if (filterOptions.minScore > 0) params.append('min_score', filterOptions.minScore.toString())
      if (filterOptions.maxPrice < 1000) params.append('max_price', filterOptions.maxPrice.toString())
      if (filterOptions.tags.length > 0) params.append('tags', filterOptions.tags.join(','))
      if (filterOptions.store !== 'all') params.append('store', filterOptions.store)
      params.append('sort_by', sortBy)
      params.append('sort_order', '-1')
      params.append('page', '1')
      params.append('limit', '100')

      const response = await axios.get(`http://localhost:8000/api/products/?${params.toString()}`)
      
      if (response.data.success) {
        setProducts(response.data.data || [])
      } else {
        setError(response.data.message || 'Failed to fetch products')
      }
    } catch (err: any) {
      console.error('Error fetching products:', err)
      if (err.response?.status === 404) {
        setError('API endpoint not found. Please check if the backend is running.')
      } else if (err.code === 'ECONNREFUSED') {
        setError('Cannot connect to backend server. Please start the backend first.')
      } else {
        setError(err.response?.data?.detail || err.message || 'Failed to fetch products')
      }
    } finally {
      setLoading(false)
    }
  }, [filterOptions, sortBy])

  const fetchStats = useCallback(async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/products/stats/overview')
      if (response.data.success) {
        return response.data.data
      }
    } catch (err) {
      console.error('Error fetching stats:', err)
    }
    return null
  }, [])

  useEffect(() => {
    fetchProducts()
  }, [fetchProducts])

  const filteredProducts = products.filter(product => {
    // Store filter
    if (filterOptions.store !== 'all' && product.source_store !== filterOptions.store) {
      return false
    }
    return true
  })

  const stats = {
    totalProducts: products.length,
    highScoreProducts: products.filter(p => p.score >= 80).length,
    averageScore: products.length > 0 ? (products.reduce((sum, p) => sum + p.score, 0) / products.length).toFixed(1) : '0',
    averagePrice: products.length > 0 ? (products.reduce((sum, p) => sum + p.price, 0) / products.length).toFixed(2) : '0',
    totalFacebookAds: products.reduce((sum, p) => sum + (p.facebook_ads?.length || 0), 0),
    totalTikTokMentions: products.reduce((sum, p) => sum + (p.tiktok_mentions?.length || 0), 0)
  }

  const updateFilterOptions = useCallback((newOptions: Partial<FilterOptions>) => {
    setFilterOptions(prev => ({ ...prev, ...newOptions }))
  }, [])

  const toggleSavedProduct = useCallback((productId: string) => {
    setSavedProducts(prev => 
      prev.includes(productId) 
        ? prev.filter(id => id !== productId)
        : [...prev, productId]
    )
  }, [])

  const clearFilters = useCallback(() => {
    setFilterOptions({
      searchTerm: '',
      category: 'all',
      minScore: 0,
      maxPrice: 1000,
      tags: [],
      store: 'all'
    })
    setSortBy('score')
  }, [])

  return {
    products,
    loading,
    error,
    filteredProducts,
    filterOptions,
    sortBy,
    viewMode,
    savedProducts,
    stats,
    setFilterOptions: updateFilterOptions,
    setSortBy,
    setViewMode,
    toggleSavedProduct,
    refreshProducts: fetchProducts,
    clearFilters
  }
} 