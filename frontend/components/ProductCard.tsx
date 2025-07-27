import { useState } from 'react'
import { 
  FireIcon, 
  ArrowTrendingUpIcon, 
  ChartBarIcon,
  CurrencyDollarIcon,
  HeartIcon,
  EyeIcon,
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

        {/* Action Buttons */}
        <div className="flex space-x-2">
          <button 
            onClick={() => onViewDetails(product)}
            className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors flex items-center justify-center space-x-1"
          >
            <EyeIcon className="w-4 h-4" />
            <span>View Details</span>
          </button>
        </div>
      </div>
    </div>
  )
} 