import { useState, useEffect, useCallback } from 'react'

export function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === 'undefined') {
      return initialValue
    }
    
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error)
      return initialValue
    }
  })

  const setValue = useCallback((value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value
      setStoredValue(valueToStore)
      
      if (typeof window !== 'undefined') {
        window.localStorage.setItem(key, JSON.stringify(valueToStore))
      }
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error)
    }
  }, [key, storedValue])

  return [storedValue, setValue] as const
}

// Specific hooks for common use cases
export function useSavedProducts() {
  return useLocalStorage<string[]>('savedProducts', [])
}

export function useUserPreferences() {
  return useLocalStorage('userPreferences', {
    theme: 'light',
    currency: 'USD',
    language: 'en',
    notifications: {
      email: true,
      push: false,
      weekly: true,
      newProducts: true
    },
    viewMode: 'grid' as 'grid' | 'list',
    defaultSort: 'score' as string,
    defaultFilters: {
      category: 'all',
      minScore: 0,
      maxPrice: 1000
    }
  })
}

export function useFilterHistory() {
  return useLocalStorage('filterHistory', [])
}

export function useRecentSearches() {
  return useLocalStorage<string[]>('recentSearches', [])
} 