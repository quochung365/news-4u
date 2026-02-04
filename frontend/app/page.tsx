'use client';

import { useState, useEffect, Suspense, useRef } from 'react';
import { useSearchParams } from 'next/navigation';
import { newsApi, NewsArticle } from '@/lib/api';
import { Search } from 'lucide-react';
import SearchBar from '@/components/SearchBar';
import Pagination from '@/components/Pagination';
import FeedManager from '../components/FeedManager';
import ArticleCard from '@/components/ArticleCard';
import ExpandedArticleView from '@/components/ExpandedArticleView';
import DarkModeToggle from '@/components/DarkModeToggle';
import { ARTICLES_PER_PAGE } from '@/lib/constants';

function HomePageContent() {
  const searchParams = useSearchParams();
  const searchBarRef = useRef<HTMLDivElement>(null);

  // State management
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState<{
    articles: boolean;
    articleId: number | null;
  }>({ articles: false, articleId: null });
  const [selectedArticle, setSelectedArticle] = useState<NewsArticle | null>(null);
  const [isSearchMode, setIsSearchMode] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchTimeFilter, setSearchTimeFilter] = useState('24h');
  const [isSearching, setIsSearching] = useState(false);
  const [searchResults, setSearchResults] = useState<NewsArticle[]>([]);
  const [searchTotal, setSearchTotal] = useState(0);
  const [selectedFeeds, setSelectedFeeds] = useState<string[]>([]);
  const [totalArticles, setTotalArticles] = useState(0);
  const [showSearchBar, setShowSearchBar] = useState(false);
  const [urlStateApplied, setUrlStateApplied] = useState(false);

  // State persistence functions
  const saveStateToStorage = () => {
    const state = {
      currentPage,
      selectedFeeds,
      isSearchMode,
      searchQuery,
      searchTimeFilter,
      searchResults: searchResults.length > 0 ? searchResults : [],
      searchTotal
    };
    localStorage.setItem('news4u_state', JSON.stringify(state));
  };

  const loadStateFromStorage = () => {
    try {
      const savedState = localStorage.getItem('news4u_state');
      if (savedState) {
        const state = JSON.parse(savedState);
        setCurrentPage(state.currentPage || 1);
        setSelectedFeeds(state.selectedFeeds || []);
        setIsSearchMode(state.isSearchMode || false);
        setSearchQuery(state.searchQuery || '');
        setSearchTimeFilter(state.searchTimeFilter || '24h');
        setSearchResults(state.searchResults || []);
        setSearchTotal(state.searchTotal || 0);
        return state;
      }
    } catch (error) {
      console.error('Error loading state from storage:', error);
    }
    return null;
  };

  const updateURLWithState = () => {
    const params = new URLSearchParams();
    if (currentPage > 1) params.set('page', currentPage.toString());
    // Only add feeds param if specific feeds are selected (not all)
    if (selectedFeeds.length > 0) params.set('feeds', selectedFeeds.join(','));
    if (isSearchMode) params.set('tab', 'search');
    if (searchQuery) params.set('q', searchQuery);
    if (searchTimeFilter !== '24h') params.set('timeFilter', searchTimeFilter);

    const newURL = params.toString() ? `/?${params.toString()}` : '/';
    window.history.replaceState({}, '', newURL);
  };

  const loadStateFromURL = () => {
    const page = parseInt(searchParams.get('page') || '1');
    const feeds = searchParams.get('feeds')?.split(',').filter(Boolean) || [];
    const tab = searchParams.get('tab') || 'news';
    const query = searchParams.get('q') || '';
    const timeFilter = searchParams.get('timeFilter') || '24h';

    setCurrentPage(page);
    setSelectedFeeds(feeds);
    setIsSearchMode(tab === 'search');
    setSearchQuery(query);
    setSearchTimeFilter(timeFilter);

    return { page, feeds, tab, query, timeFilter };
  };

  // Apply URL/Storage state once on mount. Do not fetch here — the articles effect will run after.
  useEffect(() => {
    if (urlStateApplied) return;
    const urlState = loadStateFromURL();
    if (urlState.tab === 'search' && urlState.query) {
      handleSearch(urlState.query, urlState.timeFilter);
    }
    setUrlStateApplied(true);
  }, [urlStateApplied]);

  // Single effect for loading articles: runs only after URL state is applied, and when page/feeds change.
  useEffect(() => {
    if (!urlStateApplied) return;
    if (isSearchMode) return;

    loadArticles(currentPage, selectedFeeds);
  }, [urlStateApplied, currentPage, selectedFeeds, isSearchMode]);

  // Debounce state persistence to avoid constant saves
  useEffect(() => {
    const timer = setTimeout(() => {
      saveStateToStorage();
      updateURLWithState();
    }, 500);

    return () => clearTimeout(timer);
  }, [currentPage, selectedFeeds, isSearchMode, searchQuery, searchTimeFilter]);

  // Close search bar when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchBarRef.current && !searchBarRef.current.contains(event.target as Node)) {
        // Don't close if clicking on the search icon button
        const target = event.target as HTMLElement;
        if (!target.closest('button[title="Search"]')) {
          setShowSearchBar(false);
        }
      }
    };

    if (showSearchBar) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showSearchBar]);

  const loadArticles = async (page = 1, feeds: string[] = []) => {
    try {
      setLoading(prev => ({ ...prev, articles: true }));
      const params: any = {
        page,
        per_page: ARTICLES_PER_PAGE,
      };
      // Only add feeds param if specific feeds are selected
      if (feeds.length > 0) {
        params.feeds = feeds;
      }
      const articlesData = await newsApi.getArticles(params);
      setArticles(articlesData.articles);
      setTotalArticles(articlesData.total);
      setCurrentPage(page);
    } catch (error) {
      // Error handling
    } finally {
      setLoading(prev => ({ ...prev, articles: false }));
    }
  };

  const handleArticleClick = async (article: NewsArticle) => {
    // Set the selected article to show expanded view
    setSelectedArticle(article);

    // Optionally extract content if not already processed
    if (!article.content && !article.is_processed) {
      setLoading(prev => ({ ...prev, articleId: article.id }));
      try {
        const updatedArticle = await newsApi.extractArticleContent(article.id);
        setArticles(prev => prev.map(a => a.id === article.id ? updatedArticle : a));
        setSelectedArticle(updatedArticle);
      } catch (error) {
        // Keep the original article if extraction fails
        console.error('Error extracting article content:', error);
      } finally {
        setLoading(prev => ({ ...prev, articleId: null }));
      }
    }
  };

  const handleCloseExpandedView = () => {
    setSelectedArticle(null);
  };

  const handleSearch = async (query: string, timeFilter: string) => {
    try {
      setIsSearching(true);
      setSearchQuery(query);
      setSearchTimeFilter(timeFilter);
      setCurrentPage(1);
      setIsSearchMode(true);
      setShowSearchBar(false);

      const result = await newsApi.searchArticles({
        query,
        time_filter: timeFilter,
        page: 1,
        per_page: ARTICLES_PER_PAGE
      });

      setSearchResults(result.articles);
      setSearchTotal(result.total);
      saveStateToStorage();
      updateURLWithState();
    } catch (error) {
      console.error('Search error:', error);
      setSearchResults([]);
      setSearchTotal(0);
    } finally {
      setIsSearching(false);
    }
  };

  const handleSearchPageChange = async (page: number) => {
    try {
      setIsSearching(true);
      const result = await newsApi.searchArticles({
        query: searchQuery,
        time_filter: searchTimeFilter,
        page,
        per_page: ARTICLES_PER_PAGE
      });

      setSearchResults(result.articles);
      setSearchTotal(result.total);
      setCurrentPage(page);
      saveStateToStorage();
      updateURLWithState();

      if (typeof window !== 'undefined' && window.innerWidth < 640) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    } catch (error) {
      console.error('Search page change error:', error);
    } finally {
      setIsSearching(false);
    }
  };

  const handleSearchClear = () => {
    setSearchQuery('');
    setSearchTimeFilter('24h');
    setSearchResults([]);
    setSearchTotal(0);
    setIsSearchMode(false);
    setShowSearchBar(false);
    loadArticles(1, selectedFeeds);
    saveStateToStorage();
    updateURLWithState();
  };

  const handleFeedSelectionApply = async (feeds: string[]) => {
    // Only update and reload if feeds selection actually changed
    if (JSON.stringify(feeds) === JSON.stringify(selectedFeeds)) {
      return; // No change, don't reload
    }
    
    setSelectedFeeds(feeds);
    setCurrentPage(1);
    setSearchQuery('');
    setSearchResults([]);
    setSearchTotal(0);
    setIsSearchMode(false);
    
    try {
      setLoading(prev => ({ ...prev, articles: true }));
      const params: any = {
        page: 1,
        per_page: ARTICLES_PER_PAGE,
      };
      
      // Only add feeds param if specific feeds are selected
      if (feeds.length > 0) {
        params.feeds = feeds;
      }

      const articlesData = await newsApi.getArticles(params);
      setArticles(articlesData.articles);
      setTotalArticles(articlesData.total);
      setCurrentPage(1);
      saveStateToStorage();
      updateURLWithState();
    } catch (error) {
      // Error handling
    } finally {
      setLoading(prev => ({ ...prev, articles: false }));
    }
  };

  const totalPages = Math.ceil(totalArticles / ARTICLES_PER_PAGE);

  if (loading.articles) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 dark:text-gray-400">Loading news...</p>
        </div>
      </div>
    );
  }


  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header - Always visible */}
      <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-2 sm:px-0 lg:px-6">
          <div className="flex justify-between items-center py-2 sm:py-4">
            <div className="flex items-center space-x-3 justify-between">
              <div className="mx-4">
                <a href="/" className="flex items-center space-x-3 hover:opacity-80 transition-opacity cursor-pointer">
                  <h1 className="text-xl sm:text-2xl font-bold text-primary-800 dark:text-white">News 4U</h1>
                </a>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <FeedManager
                selectedFeeds={selectedFeeds}
                onFeedSelectionApply={handleFeedSelectionApply}
              />
              <button
                onClick={() => setShowSearchBar(!showSearchBar)}
                className={`flex items-center justify-center p-2 rounded-md transition-colors ${isSearchMode || showSearchBar
                    ? 'bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300'
                    : 'bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-600'
                  }`}
                title="Search"
              >
                <Search className="h-5 w-5" />
              </button>
              <DarkModeToggle />
            </div>
          </div>
        </div>
      </header>

      {/* Search Bar Modal/Popup */}
      {showSearchBar && (
        <div ref={searchBarRef} className="max-w-7xl mx-auto px-4 sm:px-0 lg:px-6 mt-4">
          <SearchBar
            onSearch={handleSearch}
            onClear={handleSearchClear}
            isLoading={isSearching}
            initialQuery={searchQuery}
            initialTimeFilter={searchTimeFilter}
          />
        </div>
      )}

      {/* Expanded Article View */}
      {selectedArticle && (
        <ExpandedArticleView
          article={selectedArticle}
          onClose={handleCloseExpandedView}
        />
      )}

      <main className="max-w-7xl mx-auto px-0 sm:px-4 lg:px-6 py-6">
        {isSearchMode ? (
          <>

            {/* Search Results */}
            {searchResults.length > 0 ? (
              <>
                <div className="mb-4">
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Found {searchTotal} results for "{searchQuery}"
                  </p>
                </div>

                {/* Search Results Grid */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 sm:gap-6 gap-3 mb-6">
                  {searchResults.map((article) => (
                    <ArticleCard
                      key={article.id}
                      article={article}
                      onArticleClick={handleArticleClick}
                      isLoading={loading.articleId === article.id}
                    />
                  ))}
                </div>

                {/* Search Results Pagination */}
                {searchTotal > ARTICLES_PER_PAGE && (
                  <Pagination
                    currentPage={currentPage}
                    totalPages={Math.ceil(searchTotal / ARTICLES_PER_PAGE)}
                    totalItems={searchTotal}
                    itemsPerPage={ARTICLES_PER_PAGE}
                    onPageChange={handleSearchPageChange}
                  />
                )}
              </>
            ) : searchQuery && !isSearching ? (
              <div className="text-center py-12">
                <p className="text-gray-600 dark:text-gray-400">
                  No results found for "{searchQuery}"
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
                  Try adjusting your search terms or filters
                </p>
              </div>
            ) : null}
          </>
        ) : (
          <>
            {/* Article List */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 sm:gap-6 gap-3">
              {articles.map((article) => (
                <ArticleCard
                  key={article.id}
                  article={article}
                  onArticleClick={handleArticleClick}
                  isLoading={loading.articleId === article.id}
                />
              ))}
            </div>
            {/* Pagination */}
            {totalArticles > ARTICLES_PER_PAGE && (
              <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                totalItems={totalArticles}
                itemsPerPage={ARTICLES_PER_PAGE}
                onPageChange={(page) => {
                  setCurrentPage(page);
                  loadArticles(page, selectedFeeds);
                  saveStateToStorage();
                  updateURLWithState();
                  if (typeof window !== 'undefined' && window.innerWidth < 640) {
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                  }
                }}
              />
            )}
          </>
        )}
      </main>
    </div>
  );
}

export default function HomePage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 dark:text-gray-400">Loading...</p>
        </div>
      </div>
    }>
      <HomePageContent />
    </Suspense>
  );
} 