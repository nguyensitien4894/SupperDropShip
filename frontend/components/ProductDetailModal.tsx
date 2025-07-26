import { useState } from 'react'
import { 
  XMarkIcon,
  FireIcon,
  ArrowTrendingUpIcon,
  ChartBarIcon,
  CurrencyDollarIcon,
  EyeIcon,
  ShareIcon,
  StarIcon,
  SparklesIcon,
  HeartIcon,
  ClipboardDocumentIcon,
  ArrowTopRightOnSquareIcon
} from '@heroicons/react/24/outline'
import { HeartIcon as HeartIconSolid } from '@heroicons/react/24/solid'
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
  supplier_links?: any
  supplier_prices?: any
}

interface ProductDetailModalProps {
  product: Product | null
  isOpen: boolean
  onClose: () => void
  onSave: (product: Product) => void
}

export default function ProductDetailModal({ product, isOpen, onClose, onSave }: ProductDetailModalProps) {
  const [activeTab, setActiveTab] = useState<'overview' | 'analytics' | 'ai-tools'>('overview')
  const [isSaved, setIsSaved] = useState(false)
  const [aiLoading, setAiLoading] = useState(false)
  const [aiResults, setAiResults] = useState<any>({})

  if (!product || !isOpen) return null

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
    setIsSaved(!isSaved)
    onSave(product)
  }

  const generateAIContent = async (type: string) => {
    setAiLoading(true)
    try {
      const response = await axios.post(`http://localhost:8000/api/ai/${type}`, {
        text: product.title,
        purpose: type,
        tone: 'professional'
      })
      setAiResults(prev => ({
        ...prev,
        [type]: response.data.result
      }))
    } catch (error) {
      console.error('Error generating AI content:', error)
    } finally {
      setAiLoading(false)
    }
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
  }

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" onClick={onClose}></div>

        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full">
          {/* Header */}
          <div className="bg-white px-6 py-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className={`flex items-center px-3 py-1 rounded-full text-sm font-semibold border ${getScoreColor(product.score)}`}>
                  {getScoreIcon(product.score)}
                  <span className="ml-1">Score: {product.score}</span>
                </div>
                <span className="text-sm text-gray-500 capitalize">{product.category}</span>
              </div>
              <div className="flex items-center space-x-2">
                <button
                  onClick={handleSave}
                  className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                >
                  {isSaved ? (
                    <HeartIconSolid className="w-5 h-5 text-red-500" />
                  ) : (
                    <HeartIcon className="w-5 h-5" />
                  )}
                </button>
                <button
                  onClick={onClose}
                  className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                >
                  <XMarkIcon className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>

          {/* Content */}
          <div className="bg-white">
            {/* Tabs */}
            <div className="border-b border-gray-200">
              <nav className="-mb-px flex space-x-8 px-6">
                <button
                  onClick={() => setActiveTab('overview')}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'overview'
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  Overview
                </button>
                <button
                  onClick={() => setActiveTab('analytics')}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'analytics'
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  Analytics
                </button>
                <button
                  onClick={() => setActiveTab('ai-tools')}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'ai-tools'
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  AI Tools
                </button>
              </nav>
            </div>

            <div className="px-6 py-6">
              {activeTab === 'overview' && (
                <div className="space-y-6">
                  {/* Product Image and Basic Info */}
                  <div className="flex flex-col lg:flex-row gap-6">
                    <div className="lg:w-1/2">
                      <div className="h-64 bg-gradient-to-br from-blue-50 to-indigo-100 rounded-lg flex items-center justify-center">
                        <div className="text-center">
                          <div className="w-20 h-20 bg-white/80 rounded-full flex items-center justify-center mx-auto mb-4">
                            <SparklesIcon className="w-10 h-10 text-blue-600" />
                          </div>
                          <p className="text-gray-600">Product Image</p>
                        </div>
                      </div>
                    </div>
                    
                    <div className="lg:w-1/2 space-y-4">
                      <h2 className="text-2xl font-bold text-gray-900">{product.title}</h2>
                      <p className="text-gray-600">{product.description}</p>
                      
                      <div className="flex items-center space-x-4">
                        <div className="text-3xl font-bold text-gray-900">${product.price}</div>
                        {product.compare_price && product.compare_price > product.price && (
                          <div className="text-lg text-gray-500 line-through">${product.compare_price}</div>
                        )}
                        {getProfitMargin() && (
                          <div className="text-sm text-green-600 font-medium">{getProfitMargin()}% margin</div>
                        )}
                      </div>

                      <div className="flex items-center space-x-2">
                        <StarIcon className="w-5 h-5 text-yellow-400 fill-current" />
                        <span className="text-sm text-gray-600">4.8 (128 reviews)</span>
                      </div>

                      <div className="flex flex-wrap gap-2">
                        {product.tags.map((tag, index) => (
                          <span
                            key={index}
                            className="px-3 py-1 bg-blue-50 text-blue-700 text-sm rounded-full font-medium"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Stats Grid */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="bg-gray-50 p-4 rounded-lg text-center">
                      <div className="text-2xl font-bold text-blue-600">{product.facebook_ads.length}</div>
                      <div className="text-sm text-gray-600">Facebook Ads</div>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-lg text-center">
                      <div className="text-2xl font-bold text-pink-600">{product.tiktok_mentions.length}</div>
                      <div className="text-sm text-gray-600">TikTok Mentions</div>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-lg text-center">
                      <div className="text-2xl font-bold text-green-600">{product.trend_data?.trend_score || 'N/A'}</div>
                      <div className="text-sm text-gray-600">Trend Score</div>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-lg text-center">
                      <div className="text-2xl font-bold text-purple-600">{product.score}</div>
                      <div className="text-sm text-gray-600">Winning Score</div>
                    </div>
                  </div>

                  {/* Store Info */}
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h3 className="font-semibold text-gray-900 mb-2">Source Store</h3>
                    <p className="text-gray-600">{product.source_store}</p>
                  </div>
                </div>
              )}

              {activeTab === 'analytics' && (
                <div className="space-y-6">
                  <h3 className="text-lg font-semibold text-gray-900">Product Analytics</h3>
                  
                  {/* Score Breakdown */}
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h4 className="font-medium text-gray-900 mb-3">Score Breakdown</h4>
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">Facebook Ad Engagement</span>
                        <span className="text-sm font-medium">30%</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">TikTok Viral Ratio</span>
                        <span className="text-sm font-medium">25%</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">Profit Margin</span>
                        <span className="text-sm font-medium">20%</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">Google Trends Volume</span>
                        <span className="text-sm font-medium">10%</span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">Store Saturation Level</span>
                        <span className="text-sm font-medium">15%</span>
                      </div>
                    </div>
                  </div>

                  {/* Trend Data */}
                  {product.trend_data && (
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h4 className="font-medium text-gray-900 mb-3">Trend Analysis</h4>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">Trend Score:</span>
                          <span className="text-sm font-medium">{product.trend_data.trend_score}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">Search Volume:</span>
                          <span className="text-sm font-medium">{product.trend_data.search_volume}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">Growth Rate:</span>
                          <span className="text-sm font-medium">{product.trend_data.growth_rate}%</span>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {activeTab === 'ai-tools' && (
                <div className="space-y-6">
                  <h3 className="text-lg font-semibold text-gray-900">AI-Powered Tools</h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* Rewrite Title */}
                    <div className="border border-gray-200 rounded-lg p-4">
                      <h4 className="font-medium text-gray-900 mb-2">Rewrite Title</h4>
                      <button
                        onClick={() => generateAIContent('rewrite-title')}
                        disabled={aiLoading}
                        className="w-full btn-primary mb-3"
                      >
                        {aiLoading ? 'Generating...' : 'Generate New Title'}
                      </button>
                      {aiResults['rewrite-title'] && (
                        <div className="bg-blue-50 p-3 rounded-lg">
                          <p className="text-sm text-gray-900">{aiResults['rewrite-title']}</p>
                          <button
                            onClick={() => copyToClipboard(aiResults['rewrite-title'])}
                            className="mt-2 text-blue-600 hover:text-blue-700 text-sm flex items-center"
                          >
                            <ClipboardDocumentIcon className="w-4 h-4 mr-1" />
                            Copy
                          </button>
                        </div>
                      )}
                    </div>

                    {/* Generate Ad Copy */}
                    <div className="border border-gray-200 rounded-lg p-4">
                      <h4 className="font-medium text-gray-900 mb-2">Facebook Ad Copy</h4>
                      <button
                        onClick={() => generateAIContent('write-ad-copy')}
                        disabled={aiLoading}
                        className="w-full btn-primary mb-3"
                      >
                        {aiLoading ? 'Generating...' : 'Generate Ad Copy'}
                      </button>
                      {aiResults['write-ad-copy'] && (
                        <div className="bg-green-50 p-3 rounded-lg">
                          <p className="text-sm text-gray-900">{aiResults['write-ad-copy']}</p>
                          <button
                            onClick={() => copyToClipboard(aiResults['write-ad-copy'])}
                            className="mt-2 text-green-600 hover:text-green-700 text-sm flex items-center"
                          >
                            <ClipboardDocumentIcon className="w-4 h-4 mr-1" />
                            Copy
                          </button>
                        </div>
                      )}
                    </div>

                    {/* Product Description */}
                    <div className="border border-gray-200 rounded-lg p-4">
                      <h4 className="font-medium text-gray-900 mb-2">Product Description</h4>
                      <button
                        onClick={() => generateAIContent('write-description')}
                        disabled={aiLoading}
                        className="w-full btn-primary mb-3"
                      >
                        {aiLoading ? 'Generating...' : 'Generate Description'}
                      </button>
                      {aiResults['write-description'] && (
                        <div className="bg-purple-50 p-3 rounded-lg">
                          <p className="text-sm text-gray-900">{aiResults['write-description']}</p>
                          <button
                            onClick={() => copyToClipboard(aiResults['write-description'])}
                            className="mt-2 text-purple-600 hover:text-purple-700 text-sm flex items-center"
                          >
                            <ClipboardDocumentIcon className="w-4 h-4 mr-1" />
                            Copy
                          </button>
                        </div>
                      )}
                    </div>

                    {/* Why Winning */}
                    <div className="border border-gray-200 rounded-lg p-4">
                      <h4 className="font-medium text-gray-900 mb-2">Why This Product Wins</h4>
                      <button
                        onClick={() => generateAIContent('explain-why-winning')}
                        disabled={aiLoading}
                        className="w-full btn-primary mb-3"
                      >
                        {aiLoading ? 'Analyzing...' : 'Analyze Success Factors'}
                      </button>
                      {aiResults['explain-why-winning'] && (
                        <div className="bg-yellow-50 p-3 rounded-lg">
                          <p className="text-sm text-gray-900">{aiResults['explain-why-winning']}</p>
                          <button
                            onClick={() => copyToClipboard(aiResults['explain-why-winning'])}
                            className="mt-2 text-yellow-600 hover:text-yellow-700 text-sm flex items-center"
                          >
                            <ClipboardDocumentIcon className="w-4 h-4 mr-1" />
                            Copy
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Footer */}
          <div className="bg-gray-50 px-6 py-3 flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button className="btn-outline flex items-center space-x-2">
                <ShareIcon className="w-4 h-4" />
                <span>Share</span>
              </button>
              <button className="btn-outline flex items-center space-x-2">
                <ArrowTopRightOnSquareIcon className="w-4 h-4" />
                <span>View Store</span>
              </button>
            </div>
            <button
              onClick={onClose}
              className="btn-primary"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  )
} 