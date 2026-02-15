'use client';

import { useRef, useState } from 'react';
import { NewsArticle } from '@/lib/api';
import { formatRelativeTime } from '@/lib/utils';
import { X, ExternalLink, Dot } from 'lucide-react';

interface ExpandedArticleViewProps {
  article: NewsArticle;
  onClose: () => void;
}

export default function ExpandedArticleView({ article, onClose }: ExpandedArticleViewProps) {
  const [imageError, setImageError] = useState(false);
  const overlayRef = useRef<HTMLDivElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);
  const [isClosing, setIsClosing] = useState(false);

  const handleOverlayClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === overlayRef.current) {
      handleClose();
    }
  };

  const handleClose = () => {
    setIsClosing(true);
    // Small delay to allow zoom-out animation
    setTimeout(() => {
      onClose();
    }, 300);
  };

  const handleTitleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (article.link) {
      window.open(article.link, '_blank', 'noopener,noreferrer');
    }
  };

  return (
    <div
      ref={overlayRef}
      onClick={handleOverlayClick}
      className={`fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 transition-opacity duration-300 ${
        isClosing ? 'opacity-0' : 'opacity-100'
      }`}
      style={{ animation: isClosing ? 'none' : 'fadeIn 0.3s ease-out' }}
    >
      <div
        ref={contentRef}
        className={`relative bg-white dark:bg-gray-800 rounded-lg shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto transition-all duration-300 ${
          isClosing ? 'scale-95 opacity-0' : 'scale-100 opacity-100'
        }`}
        style={{ 
          animation: isClosing ? 'zoomOut 0.3s ease-in' : 'zoomIn 0.3s ease-out'
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close button - top left of card */}
        <button
          onClick={handleClose}
          className="absolute top-4 left-4 z-10 p-2 rounded-full bg-white/90 dark:bg-gray-800/90 hover:bg-white dark:hover:bg-gray-700 shadow-lg transition-colors backdrop-blur-sm"
          aria-label="Close"
        >
          <X className="h-5 w-5 text-gray-700 dark:text-gray-300" />
        </button>

        {/* Image */}
        {article.image_url && !imageError && (
          <div className="w-full h-64 sm:h-96 relative bg-gray-200 dark:bg-gray-700">
            <img
              src={article.image_url}
              alt={article.title}
              className="w-full h-full object-cover"
              onError={() => setImageError(true)}
            />
          </div>
        )}

        {/* Content */}
        <div className="p-6 sm:p-8">
          {/* Title with link */}
          <h1 className="text-xl sm:text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">
            <a
              href={article.link}
              target="_blank"
              rel="noopener noreferrer"
              onClick={handleTitleClick}
              className="hover:text-primary-600 dark:hover:text-primary-400 transition-colors flex items-center gap-2 group"
            >
              {article.title}
              <ExternalLink className="h-5 w-5 opacity-0 group-hover:opacity-100 transition-opacity" />
            </a>
          </h1>

          {/* Metadata */}
          <div className="flex flex-wrap items-center gap-2 sm:gap-1 text-sm text-gray-600 dark:text-gray-400 mb-6 pb-3 w-full border-b border-gray-200 dark:border-gray-700">
            <span className="font-medium">From {article.feed_name}</span>

            <Dot className="h-4 w-4" />
            <span>{formatRelativeTime(article.published_date || article.created_at)}</span>
          </div>

          {/* Summary */}
          {article.summary && (
            <div className="prose dark:prose-invert max-w-none">
              <p className="text-gray-700 dark:text-gray-300 text-md leading-relaxed whitespace-pre-line">
                {article.summary}
              </p>
            </div>
          )}

          {/* Content */}
          {article.content && (
            <div className="prose dark:prose-invert max-w-none">
              <p className="text-gray-700 dark:text-gray-300 text-md leading-relaxed whitespace-pre-line">
                {article.content}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
