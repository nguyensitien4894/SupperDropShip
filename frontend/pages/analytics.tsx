import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { 
  ChartBarIcon, 
  ArrowTrendingUpIcon, 
  CurrencyDollarIcon, 
  ShoppingBagIcon,
  EyeIcon,
  HeartIcon,
  ShareIcon,
  ChatBubbleLeftIcon
} from '@heroicons/react/24/outline';
import { useNotifications } from '../components/NotificationSystem';

interface AnalyticsData {
  overview: {
    total_products: number;
    total_value: number;
    average_price: number;
    total_facebook_ads: number;
    total_tiktok_mentions: number;
    total_reach: number;
    total_spend: number;
    average_engagement_rate: number;
  };
  score_distribution: {
    excellent: number;
    good: number;
    average: number;
    poor: number;
  };
  category_distribution: Record<string, number>;
  top_products: Array<{
    id: string;
    title: string;
    score: number;
    price: number;
    category: string;
  }>;
}

interface PerformanceData {
  facebook_metrics: {
    total_ads: number;
    total_reach: number;
    total_impressions: number;
    total_clicks: number;
    total_spend: number;
    avg_engagement_rate: number;
    avg_ctr: number;
    avg_cpc: number;
  };
  tiktok_metrics: {
    total_videos: number;
    total_views: number;
    total_likes: number;
    total_shares: number;
    total_comments: number;
    avg_engagement_rate: number;
  };
  performance_summary: {
    best_performing_platform: string;
    total_social_mentions: number;
    total_social_reach: number;
  };
}

interface RevenueData {
  total_revenue: number;
  total_cost: number;
  total_profit: number;
  profit_margin: number;
  avg_profit_per_product: number;
  revenue_by_category: Record<string, number>;
  profit_by_category: Record<string, number>;
  top_profitable_products: Array<{
    id: string;
    title: string;
    price: number;
    profit: number;
    profit_margin: number;
    category: string;
  }>;
}

const Analytics: React.FC = () => {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [performanceData, setPerformanceData] = useState<PerformanceData | null>(null);
  const [revenueData, setRevenueData] = useState<RevenueData | null>(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(true);
  const { addNotification } = useNotifications();

  useEffect(() => {
    fetchAnalyticsData();
  }, []);

  const fetchAnalyticsData = async () => {
    try {
      setLoading(true);
      
      // Fetch overview data
      const overviewResponse = await fetch('http://localhost:8000/api/analytics/overview');
      const overviewData = await overviewResponse.json();
      
      if (overviewData.success) {
        setAnalyticsData(overviewData.data);
      }
      
      // Fetch performance data
      const performanceResponse = await fetch('http://localhost:8000/api/analytics/performance');
      const performanceResult = await performanceResponse.json();
      
      if (performanceResult.success) {
        setPerformanceData(performanceResult.data);
      }
      
      // Fetch revenue data
      const revenueResponse = await fetch('http://localhost:8000/api/analytics/revenue');
      const revenueResult = await revenueResponse.json();
      
      if (revenueResult.success) {
        setRevenueData(revenueResult.data);
      }
      
    } catch (error) {
      console.error('Error fetching analytics data:', error);
      addNotification({
        type: 'error',
        title: 'Error',
        message: 'Failed to load analytics data'
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
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Analytics Dashboard</h1>
          <p className="text-gray-600">Comprehensive insights into your dropshipping performance</p>
        </div>

        {/* Tab Navigation */}
        <div className="mb-6">
          <nav className="flex space-x-8">
            {[
              { id: 'overview', name: 'Overview', icon: ChartBarIcon },
                             { id: 'performance', name: 'Performance', icon: ArrowTrendingUpIcon },
              { id: 'revenue', name: 'Revenue', icon: CurrencyDollarIcon }
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
        {activeTab === 'overview' && analyticsData && (
          <div className="space-y-6">
            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <div className="flex items-center">
                  <ShoppingBagIcon className="h-8 w-8 text-blue-600" />
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Total Products</p>
                    <p className="text-2xl font-bold text-gray-900">{formatNumber(analyticsData.overview.total_products)}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <div className="flex items-center">
                  <CurrencyDollarIcon className="h-8 w-8 text-green-600" />
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Total Value</p>
                    <p className="text-2xl font-bold text-gray-900">{formatCurrency(analyticsData.overview.total_value)}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <div className="flex items-center">
                  <EyeIcon className="h-8 w-8 text-purple-600" />
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Total Reach</p>
                    <p className="text-2xl font-bold text-gray-900">{formatNumber(analyticsData.overview.total_reach)}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <div className="flex items-center">
                                     <ArrowTrendingUpIcon className="h-8 w-8 text-orange-600" />
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Avg Engagement</p>
                    <p className="text-2xl font-bold text-gray-900">{formatPercentage(analyticsData.overview.average_engagement_rate)}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Score Distribution */}
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Score Distribution</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {Object.entries(analyticsData.score_distribution).map(([key, value]) => (
                  <div key={key} className="text-center">
                    <div className={`text-2xl font-bold ${
                      key === 'excellent' ? 'text-green-600' :
                      key === 'good' ? 'text-blue-600' :
                      key === 'average' ? 'text-yellow-600' : 'text-red-600'
                    }`}>
                      {value}
                    </div>
                    <div className="text-sm text-gray-600 capitalize">{key}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Category Distribution */}
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Category Distribution</h3>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {Object.entries(analyticsData.category_distribution).map(([category, count]) => (
                  <div key={category} className="text-center p-4 bg-gray-50 rounded-lg">
                    <div className="text-xl font-bold text-gray-900">{count}</div>
                    <div className="text-sm text-gray-600 capitalize">{category}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Top Products */}
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Performing Products</h3>
              <div className="space-y-3">
                {analyticsData.top_products.slice(0, 5).map((product) => (
                  <div key={product.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <p className="font-medium text-gray-900">{product.title}</p>
                      <p className="text-sm text-gray-600 capitalize">{product.category}</p>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-gray-900">{formatCurrency(product.price)}</p>
                      <p className="text-sm text-blue-600">Score: {product.score}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Performance Tab */}
        {activeTab === 'performance' && performanceData && (
          <div className="space-y-6">
            {/* Platform Comparison */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Facebook Metrics */}
              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <div className="w-3 h-3 bg-blue-600 rounded-full mr-2"></div>
                  Facebook Performance
                </h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Total Ads:</span>
                    <span className="font-medium">{formatNumber(performanceData.facebook_metrics.total_ads)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Total Reach:</span>
                    <span className="font-medium">{formatNumber(performanceData.facebook_metrics.total_reach)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Total Spend:</span>
                    <span className="font-medium">{formatCurrency(performanceData.facebook_metrics.total_spend)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Avg CTR:</span>
                    <span className="font-medium">{formatPercentage(performanceData.facebook_metrics.avg_ctr)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Avg CPC:</span>
                    <span className="font-medium">{formatCurrency(performanceData.facebook_metrics.avg_cpc)}</span>
                  </div>
                </div>
              </div>

              {/* TikTok Metrics */}
              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <div className="w-3 h-3 bg-pink-600 rounded-full mr-2"></div>
                  TikTok Performance
                </h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Total Videos:</span>
                    <span className="font-medium">{formatNumber(performanceData.tiktok_metrics.total_videos)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Total Views:</span>
                    <span className="font-medium">{formatNumber(performanceData.tiktok_metrics.total_views)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Total Likes:</span>
                    <span className="font-medium">{formatNumber(performanceData.tiktok_metrics.total_likes)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Total Shares:</span>
                    <span className="font-medium">{formatNumber(performanceData.tiktok_metrics.total_shares)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Avg Engagement:</span>
                    <span className="font-medium">{formatPercentage(performanceData.tiktok_metrics.avg_engagement_rate)}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Performance Summary */}
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Summary</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">
                    {performanceData.performance_summary.best_performing_platform}
                  </div>
                  <div className="text-sm text-gray-600">Best Platform</div>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-2xl font-bold text-green-600">
                    {formatNumber(performanceData.performance_summary.total_social_mentions)}
                  </div>
                  <div className="text-sm text-gray-600">Social Mentions</div>
                </div>
                <div className="text-center p-4 bg-purple-50 rounded-lg">
                  <div className="text-2xl font-bold text-purple-600">
                    {formatNumber(performanceData.performance_summary.total_social_reach)}
                  </div>
                  <div className="text-sm text-gray-600">Total Reach</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Revenue Tab */}
        {activeTab === 'revenue' && revenueData && (
          <div className="space-y-6">
            {/* Revenue Overview */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <div className="flex items-center">
                  <CurrencyDollarIcon className="h-8 w-8 text-green-600" />
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Total Revenue</p>
                    <p className="text-2xl font-bold text-gray-900">{formatCurrency(revenueData.total_revenue)}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <div className="flex items-center">
                  <CurrencyDollarIcon className="h-8 w-8 text-red-600" />
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Total Cost</p>
                    <p className="text-2xl font-bold text-gray-900">{formatCurrency(revenueData.total_cost)}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <div className="flex items-center">
                                     <ArrowTrendingUpIcon className="h-8 w-8 text-blue-600" />
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Total Profit</p>
                    <p className="text-2xl font-bold text-gray-900">{formatCurrency(revenueData.total_profit)}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <div className="flex items-center">
                  <ChartBarIcon className="h-8 w-8 text-purple-600" />
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600">Profit Margin</p>
                    <p className="text-2xl font-bold text-gray-900">{revenueData.profit_margin.toFixed(1)}%</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Revenue by Category */}
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Revenue by Category</h3>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {Object.entries(revenueData.revenue_by_category).map(([category, revenue]) => (
                  <div key={category} className="text-center p-4 bg-gray-50 rounded-lg">
                    <div className="text-xl font-bold text-gray-900">{formatCurrency(revenue)}</div>
                    <div className="text-sm text-gray-600 capitalize">{category}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Top Profitable Products */}
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Profitable Products</h3>
              <div className="space-y-3">
                {revenueData.top_profitable_products.slice(0, 5).map((product) => (
                  <div key={product.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <p className="font-medium text-gray-900">{product.title}</p>
                      <p className="text-sm text-gray-600 capitalize">{product.category}</p>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-green-600">{formatCurrency(product.profit)}</p>
                      <p className="text-sm text-gray-600">{product.profit_margin.toFixed(1)}% margin</p>
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

export default Analytics; 