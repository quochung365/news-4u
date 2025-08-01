'use client';

import { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { newsApi, NewsArticle } from '@/lib/api';
import { Newspaper, Search, Globe, Laptop, Flag } from 'lucide-react';
import SearchBar from '@/components/SearchBar';
import Pagination from '@/components/Pagination';
import FeedManager from '../components/FeedManager';
import ArticleCard from '@/components/ArticleCard';
import DarkModeToggle from '@/components/DarkModeToggle';
import { ARTICLES_PER_PAGE, UI_CATEGORY_MAP } from '@/lib/constants';

function HomePageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();

  // State management
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState<{
    articles: boolean;
    articleId: number | null;
  }>({ articles: false, articleId: null });
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedArticle, setSelectedArticle] = useState<NewsArticle | null>(null);
  const [activeTab, setActiveTab] = useState<'news' | 'search'>('news');
  const [currentPage, setCurrentPage] = useState(1);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchCategory, setSearchCategory] = useState('all');
  const [searchTimeFilter, setSearchTimeFilter] = useState('24h');
  const [isSearching, setIsSearching] = useState(false);
  const [searchResults, setSearchResults] = useState<NewsArticle[]>([]);
  const [searchTotal, setSearchTotal] = useState(0);
  const [selectedFeeds, setSelectedFeeds] = useState<string[]>([]);
  const [totalArticles, setTotalArticles] = useState(0);

  // State persistence functions
  const saveStateToStorage = () => {
    const state = {
      selectedCategory,
      currentPage,
      selectedFeeds,
      activeTab,
      searchQuery,
      searchCategory,
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
        setSelectedCategory(state.selectedCategory || 'all');
        setCurrentPage(state.currentPage || 1);
        setSelectedFeeds(state.selectedFeeds || []);
        setActiveTab(state.activeTab || 'news');
        setSearchQuery(state.searchQuery || '');
        setSearchCategory(state.searchCategory || 'all');
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
    if (selectedCategory !== 'all') params.set('category', selectedCategory);
    if (currentPage > 1) params.set('page', currentPage.toString());
    if (selectedFeeds.length > 0) params.set('feeds', selectedFeeds.join(','));
    if (activeTab === 'search') params.set('tab', 'search');
    if (searchQuery) params.set('q', searchQuery);
    if (searchCategory !== 'all') params.set('searchCategory', searchCategory);
    if (searchTimeFilter !== '24h') params.set('timeFilter', searchTimeFilter);

    const newURL = params.toString() ? `/?${params.toString()}` : '/';
    window.history.replaceState({}, '', newURL);
  };

  const loadStateFromURL = () => {
    const category = searchParams.get('category') || 'all';
    const page = parseInt(searchParams.get('page') || '1');
    const feeds = searchParams.get('feeds')?.split(',').filter(Boolean) || [];
    const tab = searchParams.get('tab') || 'news';
    const query = searchParams.get('q') || '';
    const searchCat = searchParams.get('searchCategory') || 'all';
    const timeFilter = searchParams.get('timeFilter') || '24h';

    setSelectedCategory(category);
    setCurrentPage(page);
    setSelectedFeeds(feeds);
    setActiveTab(tab as 'news' | 'search');
    setSearchQuery(query);
    setSearchCategory(searchCat);
    setSearchTimeFilter(timeFilter);

    return { category, page, feeds, tab, query, searchCat, timeFilter };
  };

  useEffect(() => {
    const urlState = loadStateFromURL();
    if (!urlState.category && !urlState.page && !urlState.feeds.length && !urlState.query) {
      const storageState = loadStateFromStorage();
      if (storageState) {
        if (storageState.activeTab === 'search' && storageState.searchQuery) {
          setSearchTotal(storageState.searchTotal || 0);
        } else {
          loadArticles(storageState.selectedCategory, storageState.currentPage, storageState.selectedFeeds);
        }
      } else {
        loadArticles('all', 1, []);
      }
    } else {
      if (urlState.tab === 'search' && urlState.query) {
        handleSearch(urlState.query, urlState.searchCat, urlState.timeFilter);
      } else {
        loadArticles(urlState.category, urlState.page, urlState.feeds);
      }
    }
  }, []);

  useEffect(() => {
    loadArticles(selectedCategory, currentPage, selectedFeeds);
  }, [currentPage, selectedCategory, selectedFeeds]);

  useEffect(() => {
    saveStateToStorage();
    updateURLWithState();
  }, [selectedCategory, currentPage, selectedFeeds, activeTab, searchQuery, searchCategory, searchTimeFilter]);

  const loadArticles = async (category = 'all', page = 1, feeds: string[]) => {
    try {
      setLoading(prev => ({ ...prev, articles: true }));
      const params: any = {
        page,
        per_page: ARTICLES_PER_PAGE,
        feeds: feeds,
      };
      if (category !== 'all') {
        params.category = UI_CATEGORY_MAP[category] || category;
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
    if (article.slug) {
      saveStateToStorage();
      updateURLWithState();
      router.push(`/article/${article.slug}`);
    } else {
      setLoading(prev => ({ ...prev, articleId: article.id }));
      try {
        const updatedArticle = await newsApi.extractArticleContent(article.id);
        setArticles(prev => prev.map(a => a.id === article.id ? updatedArticle : a));
        setSelectedArticle(updatedArticle);
      } catch (error) {
        setSelectedArticle(article);
      } finally {
        setLoading(prev => ({ ...prev, articleId: null }));
      }
    }
  };

  const handleExtractContent = async (articleId: number) => {
    try {
      await newsApi.extractArticleContent(articleId);
      const updatedArticle = articles.find(a => a.id === articleId);
      if (updatedArticle) {
        const response = await newsApi.getArticles({ per_page: 1, article_id: articleId });
        if (response.articles.length > 0) {
          const newArticle = response.articles[0];
          setArticles(prev => prev.map(a => a.id === articleId ? newArticle : a));
          setSelectedArticle(newArticle);
        }
      }
    } catch (error) {
      throw error;
    }
  };

  const handleSearch = async (query: string, category: string, timeFilter: string) => {
    try {
      setIsSearching(true);
      setSearchQuery(query);
      setSearchCategory(category);
      setSearchTimeFilter(timeFilter);
      setCurrentPage(1);

      const result = await newsApi.searchArticles({
        query,
        category,
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
        category: searchCategory,
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
    setSearchCategory('all');
    setSearchTimeFilter('24h');
    setSearchResults([]);
    setSearchTotal(0);
    saveStateToStorage();
    updateURLWithState();
  };

  const handleFeedSelectionApply = async (feeds: string[]) => {
    setSelectedFeeds(feeds);
    setCurrentPage(1);
    setSelectedCategory('all');
    setSearchQuery('');
    setSearchResults([]);
    setSearchTotal(0);
    setActiveTab('news');
    try {
      setLoading(prev => ({ ...prev, articles: true }));
      const params: any = {
        page: 1,
        per_page: ARTICLES_PER_PAGE,
        feeds: feeds,
      };

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

  const categories = [
    { key: 'all', label: 'All News', icon: <Newspaper className="h-4 w-4 mr-1" />, color: 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200' },
    { key: 'vn', label: 'VN', icon: <Flag className="h-4 w-4 mr-1 text-green-600 dark:text-green-300" />, color: 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200' },
    { key: 'global', label: 'Global', icon: <Globe className="h-4 w-4 mr-1 text-purple-600 dark:text-purple-300" />, color: 'bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200' },
    { key: 'us', label: 'US', icon: <Flag className="h-4 w-4 mr-1 text-red-600 dark:text-red-300" />, color: 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200' },
    { key: 'tech', label: 'Tech', icon: <Laptop className="h-4 w-4 mr-1 text-blue-600 dark:text-blue-300" />, color: 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200' },
  ];

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header - Always visible */}
      <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-2 sm:px-0 lg:px-6">
          <div className="flex justify-end items-center py-2 sm:py-4">
            <div className="flex items-center space-x-3 ">
              <div className="mx-4">
                <a href="/" className="flex items-center space-x-3 hover:opacity-80 transition-opacity cursor-pointer">
                  <h1 className="text-xl sm:text-2xl font-bold text-primary-800 dark:text-white">News 4U</h1>
                </a>
              </div>
              <FeedManager
                selectedFeeds={selectedFeeds}
                onFeedSelectionApply={handleFeedSelectionApply}
              />
              <DarkModeToggle />
            </div>
          </div>
        </div>
      </header>

      {/* Category Tabs */}
      <nav className="max-w-7xl mx-auto px-4 sm:px-0 lg:px-6 mt-4">
        <div className="flex items-center space-x-2 overflow-x-auto pb-2">
          {categories.map((cat) => (
            <button
              key={cat.key}
              onClick={() => {
                setActiveTab('news');
                setSelectedFeeds([]);
                setSelectedCategory(cat.key);
                setCurrentPage(1);
                setSearchQuery('');
                setSearchResults([]);
                setSearchTotal(0);
                loadArticles(cat.key, 1, []);
                saveStateToStorage();
                updateURLWithState();
              }}
              className={`flex items-center px-3 py-1.5 rounded-full font-medium focus:outline-none transition-all duration-150 border text-xs whitespace-nowrap shadow-sm
                ${activeTab === 'news' && selectedCategory === cat.key
                  ? `${cat.color} border-primary-600 ring-2 ring-primary-200 dark:ring-primary-700`
                  : `${cat.color} border-transparent hover:border-primary-400 hover:ring-1 hover:ring-primary-100 dark:hover:ring-primary-700`}
              `}
              style={{ minWidth: 80 }}
            >
              {cat.icon}
              {cat.label}
            </button>
          ))}
          <div className="flex-1" />
          {/* Search Tab on the far right */}
          <button
            onClick={() => {
              setActiveTab('search');
              saveStateToStorage();
              updateURLWithState();
            }}
            className={`flex items-center px-3 py-1.5 rounded-full font-medium focus:outline-none transition-all duration-150 border-2 text-xs whitespace-nowrap ml-2
              ${activeTab === 'search'
                ? 'border-primary-600 text-primary-700 dark:text-primary-300 bg-primary-50 dark:bg-gray-800 shadow-md'
                : 'border-gray-400 dark:border-gray-600 text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-800 hover:border-primary-500 hover:text-primary-700'}
            `}
            style={{ minWidth: 80 }}
          >
            <Search className="inline-block mr-1 h-4 w-4 align-text-bottom" /> Search
          </button>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-0 sm:px-4 lg:px-6 py-6">
        {activeTab === 'search' ? (
          <>
            <SearchBar
              onSearch={handleSearch}
              onClear={handleSearchClear}
              isLoading={isSearching}
              initialQuery={searchQuery}
              initialCategory={searchCategory}
              initialTimeFilter={searchTimeFilter}
            />

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
                  loadArticles(selectedCategory, page, selectedFeeds);
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