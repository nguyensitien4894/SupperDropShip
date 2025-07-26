import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { 
  ShoppingBagIcon, 
  ChartBarIcon, 
  TagIcon, 
  GlobeAltIcon,
  EyeIcon,
  CurrencyDollarIcon,
  StarIcon,
  ArrowTrendingUpIcon
} from '@heroicons/react/24/outline';
import { useNotifications } from '../components/NotificationSystem';

interface StoreData {
  store_info: {
    name: string;
    description: string;
    established: string;
    total_products: number;
    total_value: number;
    average_price: number;
  };
  performance: {
    total_facebook_ads: number;
    total_tiktok_mentions: number;
    total_reach: number;
    total_spend: number;
    average_engagement_rate: number;
  };
  categories: Record<string, number>;
  sources: Record<string, number>;
  last_updated: string;
}

interface StoreProduct {
  id: string;
  title: string;
  description: string;
  price: number;
  compare_price: number;
  score: number;
  category: string;
  tags: string[];
  source_store: string;
  source_url: string;
  image_url: string;
  facebook_ads: any[];
  tiktok_mentions: any[];
  created_at: string;
  updated_at: string;
}

interface CategoryData {
  count: number;
  total_value: number;
  avg_price: number;
  avg_score: number;
  total_engagement: number;
}

interface SourceData {
  count: number;
  total_value: number;
  avg_price: number;
  avg_score: number;
  categories: string[];
}

const Store: React.FC = () => {
  const [storeData, setStoreData] = useState<StoreData | null>(null);
  const [products, setProducts] = useState<StoreProduct[]>([]);
  const [categories, setCategories] = useState<Record<string, CategoryData>>({});
  const [sources, setSources] = useState<Record<string, SourceData>>({});
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    category: '',
    source: '',
    minScore: '',
    maxPrice: '',
    sortBy: 'score',
    sortOrder: -1
  });
  const { addNotification } = useNotifications();

  useEffect(() => {
    fetchStoreData();
  }, []);

  const fetchStoreData = async () => {
    try {
      setLoading(true);
      
      // Fetch store overview
      const overviewResponse = await fetch('http://localhost:8000/api/store/overview');
      const overviewData = await overviewResponse.json();
      
      if (overviewData.success) {
        setStoreData(overviewData.data);
      }
      
      // Fetch store products
      const productsResponse = await fetch('http://localhost:8000/api/store/products');
      const productsData = await productsResponse.json();
      
      if (productsData.success) {
        setProducts(productsData.data.products);
      }
      
      // Fetch categories
      const categoriesResponse = await fetch('http://localhost:8000/api/store/categories');
      const categoriesData = await categoriesResponse.json();
      
      if (categoriesData.success) {
        setCategories(categoriesData.data.categories);
      }
      
      // Fetch sources
      const sourcesResponse = await fetch('http://localhost:8000/api/store/sources');
      const sourcesData = await sourcesResponse.json();
      
      if (sourcesData.success) {
        setSources(sourcesData.data.sources);
      }
      
    } catch (error) {
      console.error('Error fetching store data:', error);
      addNotification({
        type: 'error',
        title: 'Error',
        message: 'Failed to load store data'
      });
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const formatNumber = (num: number) => {
    return new Intl.NumberFormat('en-US').format(num);
  };

  const formatPercentage = (num: number) => {
    return `${(num * 100).toFixed(2)}%`;
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="p-6">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Store Management</h1>
          <p className="text-gray-600">Manage your dropshipping store and view performance metrics</p>
        </div>

        {/* Tab Navigation */}
        <div className="mb-6">
          <nav className="flex space-x-8">
            {[
              { id: 'overview', name: 'Overview', icon: ShoppingBagIcon },
              { id: 'products', name: 'Products', icon: ChartBarIcon },
              { id: 'categories', name: 'Categories', icon: TagIcon },
              { id: 'sources', name: 'Sources', icon: GlobeAltIcon }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg font-medium transition-colors ${
                  activeTab === tab.id
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                <tab.icon className="h-5 w-5" />
                <span>{tab.name}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* Overview Tab */}
        {activeTab === 'overview' && storeData && (
          <div className="space-y-6">
            {/* Store Info */}
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Store Information</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="text-xl font-bold text-gray-900 mb-2">{storeData.store_info.name}</h4>
                  <p className="text-gray-600 mb-4">{storeData.store_info.description}</p>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Established:</span>
                      <span className="font-medium">{storeData.store_info.established}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Last Updated:</span>
                      <span className="font-medium">{formatDate(storeData.last_updated)}</span>
                    </div>
                  </div>
                </div>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                    <div className="flex items-center">
                      <ShoppingBagIcon className="h-6 w-6 text-blue-600 mr-2" />
                      <span className="text-gray-700">Total Products</span>
                    </div>
                    <span className="text-xl font-bold text-blue-600">{storeData.store_info.total_products}</span>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                    <div className="flex items-center">
                      <CurrencyDollarIcon className="h-6 w-6 text-green-600 mr-2" />
                      <span className="text-gray-700">Total Value</span>
                    </div>
                    <span className="text-xl font-bold text-green-600">{formatCurrency(storeData.store_info.total_value)}</span>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
                    <div className="flex items-center">
                      <StarIcon className="h-6 w-6 text-purple-600 mr-2" />
                      <span className="text-gray-700">Average Price</span>
                    </div>
                    <span className="text-xl font-bold text-purple-600">{formatCurrency(storeData.store_info.average_price)}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Performance Metrics */}
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Metrics</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">{storeData.performance.total_facebook_ads}</div>
                  <div className="text-sm text-gray-600">Facebook Ads</div>
                </div>
                <div className="text-center p-4 bg-pink-50 rounded-lg">
                  <div className="text-2xl font-bold text-pink-600">{storeData.performance.total_tiktok_mentions}</div>
                  <div className="text-sm text-gray-600">TikTok Mentions</div>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-2xl font-bold text-green-600">{formatNumber(storeData.performance.total_reach)}</div>
                  <div className="text-sm text-gray-600">Total Reach</div>
                </div>
                <div className="text-center p-4 bg-orange-50 rounded-lg">
                  <div className="text-2xl font-bold text-orange-600">{formatPercentage(storeData.performance.average_engagement_rate)}</div>
                  <div className="text-sm text-gray-600">Avg Engagement</div>
                </div>
              </div>
            </div>

            {/* Category Distribution */}
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Category Distribution</h3>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {Object.entries(storeData.categories).map(([category, count]) => (
                  <div key={category} className="text-center p-4 bg-gray-50 rounded-lg">
                    <div className="text-xl font-bold text-gray-900">{count}</div>
                    <div className="text-sm text-gray-600 capitalize">{category}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Source Distribution */}
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Source Distribution</h3>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {Object.entries(storeData.sources).map(([source, count]) => (
                  <div key={source} className="text-center p-4 bg-gray-50 rounded-lg">
                    <div className="text-xl font-bold text-gray-900">{count}</div>
                    <div className="text-sm text-gray-600">{source}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Products Tab */}
        {activeTab === 'products' && (
          <div className="space-y-6">
            {/* Filters */}
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Filters</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <select
                  value={filters.category}
                  onChange={(e) => setFilters({...filters, category: e.target.value})}
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="">All Categories</option>
                  {Object.keys(categories).map(category => (
                    <option key={category} value={category}>{category}</option>
                  ))}
                </select>
                
                <select
                  value={filters.source}
                  onChange={(e) => setFilters({...filters, source: e.target.value})}
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="">All Sources</option>
                  {Object.keys(sources).map(source => (
                    <option key={source} value={source}>{source}</option>
                  ))}
                </select>
                
                <input
                  type="number"
                  placeholder="Min Score"
                  value={filters.minScore}
                  onChange={(e) => setFilters({...filters, minScore: e.target.value})}
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
                
                <input
                  type="number"
                  placeholder="Max Price"
                  value={filters.maxPrice}
                  onChange={(e) => setFilters({...filters, maxPrice: e.target.value})}
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            </div>

            {/* Products List */}
            <div className="bg-white rounded-lg shadow-sm border">
              <div className="p-6 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900">Products ({products.length})</h3>
              </div>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Product
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Category
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Price
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Score
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Source
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Social
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {products.slice(0, 20).map((product) => (
                      <tr key={product.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <div className="flex-shrink-0 h-10 w-10">
                              <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                                <ShoppingBagIcon className="w-5 h-5 text-blue-600" />
                              </div>
                            </div>
                            <div className="ml-4">
                              <div className="text-sm font-medium text-gray-900 line-clamp-1">
                                {product.title}
                              </div>
                              <div className="text-sm text-gray-500">
                                {product.source_store}
                              </div>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800 capitalize">
                            {product.category}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {formatCurrency(product.price)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                              product.score >= 80 ? 'bg-green-100 text-green-800' :
                              product.score >= 60 ? 'bg-yellow-100 text-yellow-800' :
                              'bg-red-100 text-red-800'
                            }`}>
                              {product.score}
                            </span>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {product.source_store}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          <div className="flex space-x-2">
                            <span className="text-blue-600">{product.facebook_ads.length} FB</span>
                            <span className="text-pink-600">{product.tiktok_mentions.length} TT</span>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* Categories Tab */}
        {activeTab === 'categories' && (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Category Analysis</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {Object.entries(categories).map(([category, data]) => (
                  <div key={category} className="p-4 border border-gray-200 rounded-lg">
                    <h4 className="text-lg font-semibold text-gray-900 capitalize mb-3">{category}</h4>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Products:</span>
                        <span className="font-medium">{data.count}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Total Value:</span>
                        <span className="font-medium">{formatCurrency(data.total_value)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Avg Price:</span>
                        <span className="font-medium">{formatCurrency(data.avg_price)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Avg Score:</span>
                        <span className="font-medium">{data.avg_score.toFixed(1)}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Sources Tab */}
        {activeTab === 'sources' && (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Source Analysis</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {Object.entries(sources).map(([source, data]) => (
                  <div key={source} className="p-4 border border-gray-200 rounded-lg">
                    <h4 className="text-lg font-semibold text-gray-900 mb-3">{source}</h4>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Products:</span>
                        <span className="font-medium">{data.count}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Total Value:</span>
                        <span className="font-medium">{formatCurrency(data.total_value)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Avg Price:</span>
                        <span className="font-medium">{formatCurrency(data.avg_price)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Avg Score:</span>
                        <span className="font-medium">{data.avg_score.toFixed(1)}</span>
                      </div>
                      <div className="mt-3">
                        <span className="text-sm text-gray-600">Categories:</span>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {data.categories.map(cat => (
                            <span key={cat} className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-gray-100 text-gray-800 capitalize">
                              {cat}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
};

export default Store; 