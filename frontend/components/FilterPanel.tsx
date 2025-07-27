import { useState, useEffect } from 'react'
import { 
  FunnelIcon, 
  XMarkIcon,
  MagnifyingGlassIcon,
  AdjustmentsHorizontalIcon
} from '@heroicons/react/24/outline'
import { FilterOptions } from '../hooks/useProducts'

interface FilterPanelProps {
  filterOptions: FilterOptions
  onFilterChange: (options: Partial<FilterOptions>) => void
  onClearFilters: () => void
  categories: string[]
  availableTags: string[]
  availableStores: string[]
  isOpen: boolean
  onToggle: () => void
}

export default function FilterPanel({
  filterOptions,
  onFilterChange,
  onClearFilters,
  categories,
  availableTags,
  availableStores,
  isOpen,
  onToggle
}: FilterPanelProps) {
  const [localFilters, setLocalFilters] = useState<FilterOptions>(filterOptions)

  const handleApplyFilters = () => {
    onFilterChange(localFilters)
  }

  const handleReset = () => {
    const resetFilters: FilterOptions = {
      searchTerm: '',
      category: 'all',
      minScore: 0,
      maxPrice: 1000,
      tags: [],
      store: 'all'
    }
    setLocalFilters(resetFilters)
    onClearFilters()
  }

  const handleTagToggle = (tag: string) => {
    setLocalFilters(prev => ({
      ...prev,
      tags: prev.tags.includes(tag)
        ? prev.tags.filter(t => t !== tag)
        : [...prev.tags, tag]
    }))
  }

  const formatTagToHumanReadable = (tag: string): string => {
    // Remove store prefixes like "allbirds::", "amazon::", etc.
    const cleanTag = tag.replace(/^[a-zA-Z]+::/, '')
    
    // Convert common technical terms to human-readable format
    const tagMappings: { [key: string]: string } = {
      'carbon-score': 'Carbon Score',
      'cfld': 'Color Field',
      'complete': 'Complete',
      'edition': 'Edition',
      'gender': 'Gender',
      'hue': 'Color Hue',
      'master': 'Master Category',
      'material': 'Material',
      'price-tier': 'Price Tier',
      'msrp': 'MSRP',
      'mens': 'Men\'s',
      'womens': 'Women\'s',
      'unisex': 'Unisex',
      'limited': 'Limited Edition',
      'tree': 'Tree Material',
      'wool': 'Wool Material',
      'sugarcane': 'Sugarcane Material',
      'blue': 'Blue',
      'white': 'White',
      'black': 'Black',
      'red': 'Red',
      'green': 'Green',
      'yellow': 'Yellow',
      'purple': 'Purple',
      'orange': 'Orange',
      'pink': 'Pink',
      'gray': 'Gray',
      'brown': 'Brown',
      'mens-cruiser': 'Men\'s Cruiser',
      'womens-runner': 'Women\'s Runner',
      'unisex-sneaker': 'Unisex Sneaker',
      'true': 'Yes',
      'false': 'No'
    }
    
    // Try to find a mapping, otherwise format the tag nicely
    return tagMappings[cleanTag.toLowerCase()] || cleanTag
      .split('-')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  }

  return (
    <>
      {/* Mobile Filter Button */}
      <button
        onClick={onToggle}
        className="lg:hidden fixed bottom-6 right-6 z-40 bg-blue-600 text-white p-3 rounded-full shadow-lg hover:bg-blue-700 transition-colors"
      >
        <FunnelIcon className="w-6 h-6" />
      </button>

      {/* Mobile Filter Overlay */}
      {isOpen && (
        <div className="lg:hidden fixed inset-0 z-50">
          <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={onToggle} />
          <div className="fixed inset-y-0 right-0 flex w-80 flex-col bg-white shadow-xl">
            <div className="flex h-16 items-center justify-between px-4 border-b">
              <h2 className="text-lg font-medium text-gray-900">Filters</h2>
              <button
                onClick={onToggle}
                className="text-gray-400 hover:text-gray-600"
              >
                <XMarkIcon className="w-6 h-6" />
              </button>
            </div>
            <div className="flex-1 overflow-y-auto p-4">
              <FilterContent
                localFilters={localFilters}
                setLocalFilters={setLocalFilters}
                categories={categories}
                availableTags={availableTags}
                availableStores={availableStores}
                handleTagToggle={handleTagToggle}
                handleApplyFilters={handleApplyFilters}
                handleReset={handleReset}
                onToggle={onToggle}
                formatTagToHumanReadable={formatTagToHumanReadable}
              />
            </div>
          </div>
        </div>
      )}

      {/* Desktop Filter Panel */}
      {isOpen && (
        <div className="hidden lg:fixed lg:inset-y-0 lg:right-0 lg:flex lg:w-80 lg:flex-col lg:z-30">
          <div className="flex flex-col flex-grow bg-white border-l border-gray-200">
            <div className="flex h-16 items-center justify-between px-4 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">Filters</h2>
              <button
                onClick={onToggle}
                className="text-gray-400 hover:text-gray-600"
              >
                <XMarkIcon className="w-5 h-5" />
              </button>
            </div>
            <div className="flex-1 overflow-y-auto p-6">
              <FilterContent
                localFilters={localFilters}
                setLocalFilters={setLocalFilters}
                categories={categories}
                availableTags={availableTags}
                availableStores={availableStores}
                handleTagToggle={handleTagToggle}
                handleApplyFilters={handleApplyFilters}
                handleReset={handleReset}
                onToggle={onToggle}
                formatTagToHumanReadable={formatTagToHumanReadable}
              />
            </div>
          </div>
        </div>
      )}
    </>
  )
}

interface FilterContentProps {
  localFilters: FilterOptions
  setLocalFilters: (filters: FilterOptions) => void
  categories: string[]
  availableTags: string[]
  availableStores: string[]
  handleTagToggle: (tag: string) => void
  handleApplyFilters: () => void
  handleReset: () => void
  onToggle?: () => void
  formatTagToHumanReadable: (tag: string) => string
}

function FilterContent({
  localFilters,
  setLocalFilters,
  categories,
  availableTags,
  availableStores,
  handleTagToggle,
  handleApplyFilters,
  handleReset,
  onToggle,
  formatTagToHumanReadable
}: FilterContentProps) {
  return (
    <div className="space-y-6">
      {/* Search */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Search</label>
        <div className="relative">
          <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            value={localFilters.searchTerm}
            onChange={(e) => setLocalFilters({ ...localFilters, searchTerm: e.target.value })}
            placeholder="Search products..."
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
      </div>

      {/* Category */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Category</label>
        <select
          value={localFilters.category}
          onChange={(e) => setLocalFilters({ ...localFilters, category: e.target.value })}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="all">All Categories</option>
          {categories.map(category => (
            <option key={category} value={category}>
              {category.charAt(0).toUpperCase() + category.slice(1)}
            </option>
          ))}
        </select>
      </div>

      {/* Store */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">Store</label>
        <select
          value={localFilters.store}
          onChange={(e) => setLocalFilters({ ...localFilters, store: e.target.value })}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="all">All Stores</option>
          {availableStores.map(store => (
            <option key={store} value={store}>
              {store.replace('www.', '').replace('.com', '')}
            </option>
          ))}
        </select>
      </div>

      {/* Score Range */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Minimum Score: {localFilters.minScore}
        </label>
        <input
          type="range"
          min="0"
          max="100"
          value={localFilters.minScore}
          onChange={(e) => setLocalFilters({ ...localFilters, minScore: parseInt(e.target.value) })}
          className="w-full slider"
        />
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>0</span>
          <span>50</span>
          <span>100</span>
        </div>
      </div>

      {/* Price Range */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Max Price: ${localFilters.maxPrice}
        </label>
        <input
          type="range"
          min="0"
          max="1000"
          step="10"
          value={localFilters.maxPrice}
          onChange={(e) => setLocalFilters({ ...localFilters, maxPrice: parseInt(e.target.value) })}
          className="w-full slider"
        />
        <div className="flex justify-between text-xs text-gray-500 mt-1">
          <span>$0</span>
          <span>$500</span>
          <span>$1000</span>
        </div>
      </div>

      {/* Tags */}
      {availableTags.length > 0 && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Tags</label>
          <div className="space-y-2 max-h-32 overflow-y-auto">
            {availableTags.map(tag => (
              <label key={tag} className="flex items-center">
                <input
                  type="checkbox"
                  checked={localFilters.tags.includes(tag)}
                  onChange={() => handleTagToggle(tag)}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="ml-2 text-sm text-gray-700">{formatTagToHumanReadable(tag)}</span>
              </label>
            ))}
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="space-y-3 pt-4 border-t border-gray-200">
        <button
          onClick={handleApplyFilters}
          className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          Apply Filters
        </button>
        <button
          onClick={handleReset}
          className="w-full border border-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-50 transition-colors"
        >
          Reset All
        </button>
        {onToggle && (
          <button
            onClick={onToggle}
            className="w-full border border-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-50 transition-colors lg:hidden"
          >
            Close
          </button>
        )}
      </div>

      {/* Active Filters Summary */}
      {(localFilters.searchTerm || localFilters.category !== 'all' || localFilters.minScore > 0 || localFilters.maxPrice < 1000 || localFilters.tags.length > 0) && (
        <div className="pt-4 border-t border-gray-200">
          <h3 className="text-sm font-medium text-gray-700 mb-2">Active Filters</h3>
          <div className="space-y-1">
            {localFilters.searchTerm && (
              <div className="text-xs text-gray-600">Search: "{localFilters.searchTerm}"</div>
            )}
            {localFilters.category !== 'all' && (
              <div className="text-xs text-gray-600">Category: {localFilters.category}</div>
            )}
            {localFilters.minScore > 0 && (
              <div className="text-xs text-gray-600">Min Score: {localFilters.minScore}</div>
            )}
            {localFilters.maxPrice < 1000 && (
              <div className="text-xs text-gray-600">Max Price: ${localFilters.maxPrice}</div>
            )}
            {localFilters.tags.length > 0 && (
              <div className="text-xs text-gray-600">Tags: {localFilters.tags.join(', ')}</div>
            )}
          </div>
        </div>
      )}
    </div>
  )
} 