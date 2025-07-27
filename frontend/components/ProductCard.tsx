import { useState } from 'react'
import { 
  FireIcon, 
  ArrowTrendingUpIcon, 
  ChartBarIcon,
  CurrencyDollarIcon,
  HeartIcon,
  EyeIcon,
  ShareIcon,
  StarIcon,
  SparklesIcon,
  ShoppingBagIcon
} from '@heroicons/react/24/outline'
import { HeartIcon as HeartIconSolid } from '@heroicons/react/24/solid'

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
  source_url?: string
  image_url?: string
  facebook_ads: any[]
  tiktok_mentions: any[]
  trend_data: any
  supplier_links?: any
  supplier_prices?: any
}

interface ProductCardProps {
  product: Product
  onViewDetails: (product: Product) => void
  onSave: (product: Product) => void
  onShare?: () => void
  isSaved?: boolean
}

export default function ProductCard({ product, onViewDetails, onSave, onShare, isSaved: externalIsSaved }: ProductCardProps) {
  const [internalIsSaved, setInternalIsSaved] = useState(false)
  const [isHovered, setIsHovered] = useState(false)
  
  const isSaved = externalIsSaved !== undefined ? externalIsSaved : internalIsSaved

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-100 border-green-200'
    if (score >= 60) return 'text-yellow-600 bg-yellow-100 border-yellow-200'
    return 'text-red-600 bg-red-100 border-red-200'
  }

  const getScoreIcon = (score: number) => {
    if (score >= 80) return <FireIcon className="w-4 h-4" />
    if (score >= 60) return <ArrowTrendingUpIcon className="w-4 h-4" />
    return <ChartBarIcon className="w-4 h-4" />
  }

  const getProfitMargin = () => {
    if (!product.supplier_prices) return null
    const supplierPrice = Math.min(...Object.values(product.supplier_prices) as number[])
    const margin = ((product.price - supplierPrice) / product.price) * 100
    return margin.toFixed(1)
  }

  const getStoreInfo = () => {
    const storeInfo = []
    
    // Source store
    if (product.source_store) {
      storeInfo.push({
        label: 'Source Store',
        value: product.source_store,
        type: 'store'
      })
    }
    
    // Source URL
    if (product.source_url) {
      storeInfo.push({
        label: 'Product URL',
        value: product.source_url,
        type: 'url'
      })
    }
    
    // Supplier links
    if (product.supplier_links && Object.keys(product.supplier_links).length > 0) {
      Object.entries(product.supplier_links).forEach(([platform, url]) => {
        storeInfo.push({
          label: `${platform.charAt(0).toUpperCase() + platform.slice(1)}`,
          value: url,
          type: 'supplier'
        })
      })
    }
    
    // Supplier prices
    if (product.supplier_prices && Object.keys(product.supplier_prices).length > 0) {
      Object.entries(product.supplier_prices).forEach(([platform, price]) => {
        storeInfo.push({
          label: `${platform.charAt(0).toUpperCase() + platform.slice(1)} Price`,
          value: `$${price}`,
          type: 'price'
        })
      })
    }
    
    return storeInfo
  }

  const getStoreIcon = (storeName: string) => {
    const store = storeName.toLowerCase()
    if (store.includes('aliexpress')) {
      return (
        <div className="w-6 h-6 bg-orange-500 rounded flex items-center justify-center">
          <span className="text-white text-xs font-bold">A</span>
        </div>
      )
    }
    if (store.includes('amazon')) {
      return (
        <div className="w-6 h-6 bg-yellow-500 rounded flex items-center justify-center">
          <span className="text-white text-xs font-bold">A</span>
        </div>
      )
    }
    if (store.includes('shopify') || store.includes('allbirds') || store.includes('glossier') || store.includes('awaytravel') || store.includes('kyliecosmetics')) {
      return (
        <div className="w-6 h-6 bg-green-500 rounded flex items-center justify-center">
          <span className="text-white text-xs font-bold">S</span>
        </div>
      )
    }
    if (store.includes('temu')) {
      return (
        <div className="w-6 h-6 bg-red-500 rounded flex items-center justify-center">
          <span className="text-white text-xs font-bold">T</span>
        </div>
      )
    }
    // Default store icon
    return (
      <div className="w-6 h-6 bg-gray-500 rounded flex items-center justify-center">
        <span className="text-white text-xs font-bold">S</span>
      </div>
    )
  }

  const getStoreName = (storeName: string) => {
    const store = storeName.toLowerCase()
    if (store.includes('aliexpress')) return 'AliExpress'
    if (store.includes('amazon')) return 'Amazon'
    if (store.includes('shopify') || store.includes('allbirds') || store.includes('glossier') || store.includes('awaytravel') || store.includes('kyliecosmetics')) return 'Shopify'
    if (store.includes('temu')) return 'Temu'
    return storeName
  }

  const handleSave = () => {
    if (externalIsSaved === undefined) {
      setInternalIsSaved(!internalIsSaved)
    }
    onSave(product)
  }

  return (
    <div 
      className={`bg-white rounded-xl shadow-sm border border-gray-200 hover:shadow-lg transition-all duration-300 overflow-hidden group ${
        isHovered ? 'transform -translate-y-1' : ''
      }`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Product Image */}
      <div className="relative h-48 bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center overflow-hidden">
        {product.image_url ? (
          <img 
            src={product.image_url} 
            alt={product.title}
            className="w-full h-full object-cover"
            onError={(e) => {
              e.currentTarget.style.display = 'none';
              e.currentTarget.nextElementSibling?.classList.remove('hidden');
            }}
          />
        ) : null}
        <div className={`absolute inset-0 bg-gradient-to-br from-blue-500/10 to-purple-500/10 flex items-center justify-center ${product.image_url ? 'hidden' : ''}`}>
          <div className="relative z-10 text-center">
            <div className="w-16 h-16 bg-white/80 rounded-full flex items-center justify-center mx-auto mb-2">
              <SparklesIcon className="w-8 h-8 text-blue-600" />
            </div>
            <p className="text-sm text-gray-600 font-medium">Product Image</p>
          </div>
        </div>
        
        {/* Score Badge */}
        <div className={`absolute top-3 right-3 flex items-center px-2 py-1 rounded-full text-xs font-semibold border ${getScoreColor(product.score)}`}>
          {getScoreIcon(product.score)}
          <span className="ml-1">{product.score}</span>
        </div>

        {/* Save Button */}
        <button
          onClick={handleSave}
          className="absolute top-3 left-3 p-2 rounded-full bg-white/80 hover:bg-white transition-colors"
        >
          {isSaved ? (
            <HeartIconSolid className="w-5 h-5 text-red-500" />
          ) : (
            <HeartIcon className="w-5 h-5 text-gray-600" />
          )}
        </button>
      </div>

      {/* Product Content */}
      <div className="p-6">
        {/* Title and Category */}
        <div className="mb-3">
          <h3 className="text-lg font-semibold text-gray-900 line-clamp-2 mb-1 group-hover:text-blue-600 transition-colors">
            {product.title}
          </h3>
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-500 capitalize">{product.category}</span>
            <div className="flex items-center space-x-1">
              <StarIcon className="w-4 h-4 text-yellow-400 fill-current" />
              <span className="text-sm text-gray-600">4.8</span>
            </div>
          </div>
        </div>

        {/* Description */}
        <p className="text-sm text-gray-600 line-clamp-2 mb-4">
          {product.description}
        </p>

        {/* Price Section */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <span className="text-2xl font-bold text-gray-900">
              ${product.price}
            </span>
            {product.compare_price && product.compare_price > product.price && (
              <span className="text-sm text-gray-500 line-through">
                ${product.compare_price}
              </span>
            )}
          </div>
          <div className="flex items-center space-x-1 text-green-600">
            <CurrencyDollarIcon className="w-5 h-5" />
            {getProfitMargin() && (
              <span className="text-sm font-medium">{getProfitMargin()}% margin</span>
            )}
          </div>
        </div>

        {/* Store Information */}
        <div className="mt-4">
          <h4 className="text-sm font-semibold text-gray-800 mb-2">Store Information</h4>
          <div className="grid grid-cols-2 gap-2 text-sm text-gray-700">
            {getStoreInfo().map((item, index) => (
              <div key={index} className="flex items-center space-x-2">
                {item.type === 'store' && getStoreIcon(item.value)}
                {item.type === 'url' && <ShoppingBagIcon className="w-4 h-4 text-blue-500" />}
                {item.type === 'supplier' && <HeartIcon className="w-4 h-4 text-purple-500" />}
                {item.type === 'price' && <CurrencyDollarIcon className="w-4 h-4 text-green-500" />}
                <span>{item.label}:</span>
                <span className="font-medium">{item.value}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 gap-3 mb-4 text-sm">
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
            <span className="text-gray-500">Facebook Ads:</span>
            <span className="font-medium">{product.facebook_ads.length}</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-pink-500 rounded-full"></div>
            <span className="text-gray-500">TikTok:</span>
            <span className="font-medium">{product.tiktok_mentions.length}</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span className="text-gray-500">Store:</span>
            <div className="flex items-center space-x-1">
              {getStoreIcon(product.source_store)}
              <span className="font-medium text-sm">{getStoreName(product.source_store)}</span>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
            <span className="text-gray-500">Trend:</span>
            <span className="font-medium">{product.trend_data?.trend_score || 'N/A'}</span>
          </div>
        </div>

        {/* Tags */}
        {product.tags.length > 0 && (
          <div className="mb-4">
            <div className="flex flex-wrap gap-1">
              {product.tags.slice(0, 3).map((tag, index) => (
                <span
                  key={index}
                  className="px-2 py-1 bg-blue-50 text-blue-700 text-xs rounded-full font-medium"
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
        <div className="flex space-x-2">
          <button 
            onClick={() => onViewDetails(product)}
            className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors flex items-center justify-center space-x-1"
          >
            <EyeIcon className="w-4 h-4" />
            <span>View Details</span>
          </button>
          {product.source_url && (
            <button 
              onClick={() => window.open(product.source_url, '_blank')}
              className="flex-1 bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-green-700 transition-colors flex items-center justify-center space-x-1"
            >
              <ShoppingBagIcon className="w-4 h-4" />
              <span>View Store</span>
            </button>
          )}
          <button 
            onClick={onShare}
            className="p-2 border border-gray-300 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors"
          >
            <ShareIcon className="w-4 h-4 text-gray-600" />
          </button>
        </div>
      </div>
    </div>
  )
} 