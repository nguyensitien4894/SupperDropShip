import { useState, useEffect } from 'react'
import { 
  MagnifyingGlassIcon, 
  ChartBarIcon, 
  SparklesIcon,
  FireIcon,
  CurrencyDollarIcon,
  TrendingUpIcon
} from '@heroicons/react/24/outline'
import axios from 'axios'

interface Product {
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
}

export default function Dashboard() {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [minScore, setMinScore] = useState(0)

  useEffect(() => {
    fetchProducts()
  }, [])

  const fetchProducts = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/products/')
      setProducts(response.data.data || [])
    } catch (error) {
      console.error('Error fetching products:', error)
    } finally {
      setLoading(false)
    }
  }

  const filteredProducts = products.filter(product => {
    const matchesSearch = product.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         product.description.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCategory = selectedCategory === 'all' || product.category === selectedCategory
    const matchesScore = product.score >= minScore
    return matchesSearch && matchesCategory && matchesScore
  })

  const categories = ['all', 'gadgets', 'home', 'fashion', 'beauty', 'fitness', 'pets', 'kids', 'automotive', 'garden', 'sports']

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-100'
    if (score >= 60) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const getScoreIcon = (score: number) => {
    if (score >= 80) return <FireIcon className="w-4 h-4" />
    if (score >= 60) return <TrendingUpIcon className="w-4 h-4" />
    return <ChartBarIcon className="w-4 h-4" />
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <SparklesIcon className="w-8 h-8 text-blue-600" />
              <h1 className="ml-3 text-2xl font-bold text-gray-900">
                Dropship Intelligence
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500">Discover Winning Products</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {/* Search */}
            <div className="relative">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search products..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            {/* Category Filter */}
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            >
              {categories.map(category => (
                <option key={category} value={category}>
                  {category === 'all' ? 'All Categories' : category.charAt(0).toUpperCase() + category.slice(1)}
                </option>
              ))}
            </select>

            {/* Min Score Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Min Score: {minScore}
              </label>
              <input
                type="range"
                min="0"
                max="100"
                value={minScore}
                onChange={(e) => setMinScore(parseInt(e.target.value))}
                className="w-full"
              />
            </div>

            {/* Results Count */}
            <div className="flex items-center justify-end">
              <span className="text-sm text-gray-500">
                {filteredProducts.length} products found
              </span>
            </div>
          </div>
        </div>

        {/* Products Grid */}
        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredProducts.map((product) => (
              <div key={product.id} className="bg-white rounded-lg shadow-sm border hover:shadow-md transition-shadow">
                {/* Product Header */}
                <div className="p-6 border-b">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="text-lg font-semibold text-gray-900 line-clamp-2">
                      {product.title}
                    </h3>
                    <div className={`flex items-center px-2 py-1 rounded-full text-xs font-medium ${getScoreColor(product.score)}`}>
                      {getScoreIcon(product.score)}
                      <span className="ml-1">{product.score}</span>
                    </div>
                  </div>
                  
                  <p className="text-sm text-gray-600 line-clamp-2 mb-3">
                    {product.description}
                  </p>

                  {/* Price */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <span className="text-2xl font-bold text-gray-900">
                        ${product.price}
                      </span>
                      {product.compare_price && (
                        <span className="text-sm text-gray-500 line-through">
                          ${product.compare_price}
                        </span>
                      )}
                    </div>
                    <CurrencyDollarIcon className="w-5 h-5 text-green-600" />
                  </div>
                </div>

                {/* Product Stats */}
                <div className="p-6">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-500">Category:</span>
                      <span className="ml-1 font-medium capitalize">{product.category}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Store:</span>
                      <span className="ml-1 font-medium">{product.source_store}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Facebook Ads:</span>
                      <span className="ml-1 font-medium">{product.facebook_ads.length}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">TikTok Mentions:</span>
                      <span className="ml-1 font-medium">{product.tiktok_mentions.length}</span>
                    </div>
                  </div>

                  {/* Tags */}
                  {product.tags.length > 0 && (
                    <div className="mt-4">
                      <div className="flex flex-wrap gap-1">
                        {product.tags.slice(0, 3).map((tag, index) => (
                          <span
                            key={index}
                            className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                          >
                            {tag}
                          </span>
                        ))}
                        {product.tags.length > 3 && (
                          <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
                            +{product.tags.length - 3}
                          </span>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Action Buttons */}
                  <div className="mt-4 flex space-x-2">
                    <button className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors">
                      View Details
                    </button>
                    <button className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium hover:bg-gray-50 transition-colors">
                      Save
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Empty State */}
        {!loading && filteredProducts.length === 0 && (
          <div className="text-center py-12">
            <SparklesIcon className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No products found</h3>
            <p className="mt-1 text-sm text-gray-500">
              Try adjusting your search criteria or filters.
            </p>
          </div>
        )}
      </main>
    </div>
  )
} 