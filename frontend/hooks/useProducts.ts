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
    tags: []
  })
  const [sortBy, setSortBy] = useState<SortOption>('score')
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [savedProducts, setSavedProducts] = useState<string[]>([])

  const fetchProducts = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await axios.get('http://localhost:8000/api/products/')
      setProducts(response.data.data || [])
    } catch (err) {
      setError('Failed to fetch products')
      console.error('Error fetching products:', err)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchProducts()
  }, [fetchProducts])

  const filteredProducts = products
    .filter(product => {
      const matchesSearch = product.title.toLowerCase().includes(filterOptions.searchTerm.toLowerCase()) ||
                           product.description.toLowerCase().includes(filterOptions.searchTerm.toLowerCase())
      const matchesCategory = filterOptions.category === 'all' || product.category === filterOptions.category
      const matchesScore = product.score >= filterOptions.minScore
      const matchesPrice = product.price <= filterOptions.maxPrice
      const matchesTags = filterOptions.tags.length === 0 || 
                         filterOptions.tags.some(tag => product.tags.includes(tag))
      
      return matchesSearch && matchesCategory && matchesScore && matchesPrice && matchesTags
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'score':
          return b.score - a.score
        case 'price':
          return a.price - b.price
        case 'price_high':
          return b.price - a.price
        case 'trend':
          return (b.trend_data?.trend_score || 0) - (a.trend_data?.trend_score || 0)
        case 'newest':
          return new Date(b.created_at || 0).getTime() - new Date(a.created_at || 0).getTime()
        case 'name':
          return a.title.localeCompare(b.title)
        default:
          return 0
      }
    })

  const stats = {
    totalProducts: products.length,
    highScoreProducts: products.filter(p => p.score >= 80).length,
    averageScore: products.length > 0 ? (products.reduce((sum, p) => sum + p.score, 0) / products.length).toFixed(1) : '0',
    averagePrice: products.length > 0 ? (products.reduce((sum, p) => sum + p.price, 0) / products.length).toFixed(2) : '0',
    totalFacebookAds: products.reduce((sum, p) => sum + p.facebook_ads.length, 0),
    totalTikTokMentions: products.reduce((sum, p) => sum + p.tiktok_mentions.length, 0)
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
      tags: []
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