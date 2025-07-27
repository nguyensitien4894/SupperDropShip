import { useState } from 'react'
import { 
  MagnifyingGlassIcon, 
  FunnelIcon,
  SparklesIcon,
  FireIcon,
  CurrencyDollarIcon,
  ArrowTrendingUpIcon,
  ChartBarIcon,
  EyeIcon,
  HeartIcon,
  ShareIcon,
  StarIcon,
  XMarkIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline'
import { HeartIcon as HeartIconSolid } from '@heroicons/react/24/solid'
import Layout from '../components/Layout'
import ProductCard from '../components/ProductCard'
import ProductDetailModal from '../components/ProductDetailModal'
import FilterPanel from '../components/FilterPanel'
import { useProducts, Product } from '../hooks/useProducts'
import { useNotifications, notificationUtils } from '../components/NotificationSystem'
import { useSavedProducts } from '../hooks/useLocalStorage'
import axios from 'axios'

export default function Dashboard() {
  const {
    filteredProducts,
    loading,
    error,
    filterOptions,
    sortBy,
    viewMode,
    stats,
    setFilterOptions,
    setSortBy,
    setViewMode,
    toggleSavedProduct,
    refreshProducts,
    clearFilters
  } = useProducts()

  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null)
  const [showFilters, setShowFilters] = useState(false)
  const [savedProducts, setSavedProducts] = useSavedProducts()
  const { addNotification } = useNotifications()

  const categories = ['all', 'gadgets', 'home', 'fashion', 'beauty', 'fitness', 'pets', 'kids', 'automotive', 'garden', 'sports']
  
  // Get unique tags from all products
  const availableTags = Array.from(new Set(
    filteredProducts.flatMap(product => product.tags)
  )).sort()

  // Get unique stores from all products, filter to show only amazon, aliexpress, shopify
  const allStores = Array.from(new Set(
    filteredProducts.map(product => product.source_store)
  )).sort()
  
  const availableStores = allStores.filter(store => {
    const storeLower = store.toLowerCase()
    // Show popular platforms: amazon, aliexpress, shopify, etsy, alibaba, taobao, temu, wish, ebay
    return storeLower === 'amazon.com' || 
           storeLower === 'aliexpress' || 
           storeLower === 'shopify' ||
           storeLower === 'amazon' ||
           storeLower === 'aliexpress.com' ||
           storeLower === 'shopify.com' ||
           storeLower === 'etsy' ||
           storeLower === 'etsy.com' ||
           storeLower === 'alibaba' ||
           storeLower === 'alibaba.com' ||
           storeLower === 'taobao' ||
           storeLower === 'taobao.com' ||
           storeLower === 'temu' ||
           storeLower === 'temu.com' ||
           storeLower === 'wish' ||
           storeLower === 'wish.com' ||
           storeLower === 'ebay' ||
           storeLower === 'ebay.com' ||
           storeLower === 'walmart' ||
           storeLower === 'walmart.com' ||
           storeLower === 'target' ||
           storeLower === 'target.com' ||
           storeLower === 'bestbuy' ||
           storeLower === 'bestbuy.com'
  })

  const handleViewDetails = (product: Product) => {
    setSelectedProduct(product)
  }

  const handleSaveProduct = (product: Product) => {
    toggleSavedProduct(product.id)
    const isSaved = savedProducts.includes(product.id)
    
    if (isSaved) {
      setSavedProducts(prev => prev.filter(id => id !== product.id))
      addNotification(notificationUtils.success(
        'Product Removed',
        `${product.title} has been removed from your saved products.`
      ))
    } else {
      setSavedProducts(prev => [...prev, product.id])
      addNotification(notificationUtils.success(
        'Product Saved',
        `${product.title} has been added to your saved products.`
      ))
    }
  }

  const handleRefresh = async () => {
    try {
      await refreshProducts()
      addNotification(notificationUtils.success(
        'Data Refreshed',
        'Product data has been updated successfully.'
      ))
    } catch (err) {
      addNotification(notificationUtils.error(
        'Refresh Failed',
        'Failed to refresh product data. Please try again.'
      ))
    }
  }

  const handleShare = async (product: Product) => {
    try {
      await navigator.share({
        title: product.title,
        text: product.description,
        url: window.location.href
      })
      addNotification(notificationUtils.success(
        'Shared Successfully',
        `${product.title} has been shared.`
      ))
    } catch (err) {
      addNotification(notificationUtils.error(
        'Share Failed',
        'Failed to share product. Please try again.'
      ))
    }
  }

  const handleCrawlProducts = async () => {
    try {
      addNotification(notificationUtils.info(
        'Crawling Started',
        'Starting to crawl products from multiple sources...'
      ))
      
      const response = await axios.post('http://localhost:8000/api/products/crawl/start?max_products_per_source=20')
      
      if (response.data.success) {
        addNotification(notificationUtils.success(
          'Crawl Completed',
          `Successfully crawled ${response.data.data.total_products} products from multiple sources.`
        ))
        
        // Refresh the products list
        await refreshProducts()
      } else {
        throw new Error('Crawl failed')
      }
    } catch (err) {
      addNotification(notificationUtils.error(
        'Crawl Failed',
        'Failed to crawl products. Please try again.'
      ))
    }
  }

  if (error) {
    return (
      <Layout>
        <div className="text-center py-12">
          <div className="mx-auto h-24 w-24 bg-red-100 rounded-full flex items-center justify-center mb-4">
            <XMarkIcon className="h-12 w-12 text-red-600" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">Error Loading Data</h3>
          <p className="text-gray-500 mb-6">{error}</p>
          <button
            onClick={handleRefresh}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </Layout>
    )
  }

  return (
    <Layout showFilters={showFilters}>
      {/* Header */}
      <div className="mb-8">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
            <p className="mt-2 text-gray-600">Discover winning dropshipping products with AI-powered insights</p>
          </div>
          <div className="mt-4 sm:mt-0 flex items-center space-x-3">
            <button
              onClick={handleCrawlProducts}
              disabled={loading}
              className="p-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50 bg-green-50 hover:bg-green-100"
              title="Crawl New Products"
            >
              <SparklesIcon className="w-5 h-5 text-green-600" />
            </button>
            <button
              onClick={handleRefresh}
              disabled={loading}
              className="p-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50"
            >
              <ArrowPathIcon className={`w-5 h-5 text-gray-600 ${loading ? 'animate-spin' : ''}`} />
            </button>
            <button
              onClick={() => setViewMode(viewMode === 'grid' ? 'list' : 'grid')}
              className="p-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              {viewMode === 'grid' ? (
                <ChartBarIcon className="w-5 h-5 text-gray-600" />
              ) : (
                <SparklesIcon className="w-5 h-5 text-gray-600" />
              )}
            </button>
            <button
              onClick={() => setShowFilters(!showFilters)}
              className={`px-4 py-2 border border-gray-300 rounded-lg transition-colors flex items-center space-x-2 ${
                showFilters 
                  ? 'bg-blue-600 text-white border-blue-600 hover:bg-blue-700' 
                  : 'bg-white text-gray-700 hover:bg-gray-50'
              }`}
            >
              <FunnelIcon className="w-5 h-5" />
              <span className="hidden sm:inline">Filter</span>
            </button>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <SparklesIcon className="w-6 h-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Products</p>
              <p className="text-2xl font-bold text-gray-900">{stats.totalProducts}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <FireIcon className="w-6 h-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">High Score</p>
              <p className="text-2xl font-bold text-gray-900">{stats.highScoreProducts}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center">
            <div className="p-2 bg-yellow-100 rounded-lg">
              <ArrowTrendingUpIcon className="w-6 h-6 text-yellow-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Avg Score</p>
              <p className="text-2xl font-bold text-gray-900">{stats.averageScore}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <EyeIcon className="w-6 h-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Facebook Ads</p>
              <p className="text-2xl font-bold text-gray-900">{stats.totalFacebookAds}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center">
            <div className="p-2 bg-pink-100 rounded-lg">
              <ShareIcon className="w-6 h-6 text-pink-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">TikTok Mentions</p>
              <p className="text-2xl font-bold text-gray-900">{stats.totalTikTokMentions}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0 lg:space-x-4">
          {/* Search */}
          <div className="flex-1 relative">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search products by title or description..."
              value={filterOptions.searchTerm}
              onChange={(e) => setFilterOptions({ searchTerm: e.target.value })}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            />
          </div>

          {/* Sort */}
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
          >
            <option value="score">Sort by Score</option>
            <option value="price">Price: Low to High</option>
            <option value="price_high">Price: High to Low</option>
            <option value="trend">Trend Score</option>
            <option value="newest">Newest First</option>
            <option value="name">Name A-Z</option>
          </select>

          {/* Results Count */}
          <div className="flex items-center justify-between lg:justify-end">
            <span className="text-sm text-gray-500">
              {filteredProducts.length} products found
            </span>
          </div>
        </div>
      </div>

      {/* Filter Panel */}
      <FilterPanel
        filterOptions={filterOptions}
        onFilterChange={setFilterOptions}
        onClearFilters={clearFilters}
        categories={categories}
        availableTags={availableTags}
        availableStores={availableStores}
        isOpen={showFilters}
        onToggle={() => setShowFilters(!showFilters)}
      />

      {/* Products Grid/List */}
      {loading ? (
        <div className="flex justify-center items-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      ) : (
        <div className={viewMode === 'grid' 
          ? "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
          : "space-y-4"
        }>
          {filteredProducts.map((product) => (
            <ProductCard
              key={product.id}
              product={product}
              onViewDetails={handleViewDetails}
              onSave={handleSaveProduct}
              onShare={() => handleShare(product)}
              isSaved={savedProducts.includes(product.id)}
            />
          ))}
        </div>
      )}

      {/* Empty State */}
      {!loading && filteredProducts.length === 0 && (
        <div className="text-center py-12">
          <div className="mx-auto h-24 w-24 bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <SparklesIcon className="h-12 w-12 text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No products found</h3>
          <p className="text-gray-500 mb-6">
            Try adjusting your search criteria or filters to find more products.
          </p>
          <button
            onClick={clearFilters}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Clear Filters
          </button>
        </div>
      )}

      {/* Product Detail Modal */}
      {selectedProduct && (
        <ProductDetailModal
          product={selectedProduct}
          isOpen={!!selectedProduct}
          onClose={() => setSelectedProduct(null)}
          onSave={handleSaveProduct}
        />
      )}
    </Layout>
  )
} 