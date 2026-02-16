# News 4U Frontend

Modern, responsive Next.js frontend for the News 4U RSS aggregator platform.

## Tech Stack

- **Framework**: Next.js 14.2.30 (React 18)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Date Handling**: date-fns

## Features

- **Article Browsing**: Browse news articles with pagination
- **Feed Filtering**: Filter articles by RSS feeds
- **Search**: Full-text search with time filters
- **Article View**: Expanded view with full article content
- **Dark Mode**: Toggle between light and dark themes
- **Responsive Design**: Optimized for mobile, tablet, and desktop
- **State Persistence**: Maintains browsing state across sessions

## Project Structure

```
frontend/
├── app/                      # Next.js app directory
│   ├── layout.tsx           # Root layout with metadata
│   └── page.tsx             # Main home page component
├── components/              # React components
│   ├── ArticleCard.tsx      # Article preview card
│   ├── ExpandedArticleView.tsx  # Full article modal
│   ├── FeedManager.tsx      # Feed selection modal
│   ├── SearchBar.tsx        # Search interface
│   ├── Pagination.tsx       # Pagination controls
│   ├── DarkModeToggle.tsx   # Dark mode toggle button
│   └── Footer.tsx           # Page footer
├── lib/                     # Utilities and configuration
│   ├── api.ts              # API client and types
│   ├── constants.ts        # Application constants
│   ├── utils.ts            # Utility functions
│   └── darkMode.tsx        # Dark mode context provider
├── public/                  # Static assets
├── package.json            # Dependencies and scripts
├── tsconfig.json           # TypeScript configuration
├── tailwind.config.js      # Tailwind CSS configuration
├── postcss.config.js       # PostCSS configuration
└── next.config.js          # Next.js configuration
```

## Getting Started

### Prerequisites

- Node.js 18.0 or higher
- npm or yarn package manager
- Backend API running (see [../backend/README.md](../backend/README.md))

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create environment configuration:
```bash
# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at [http://localhost:3000](http://localhost:3000)

### Build for Production

```bash
# Build the application
npm run build

# Start production server
npm start
```

## Components Overview

### Core Components

#### `app/page.tsx`
Main application component that orchestrates all functionality:
- Article fetching and display
- Search functionality
- Feed filtering
- State management and persistence
- URL state synchronization

#### `ArticleCard.tsx`
Displays article preview with:
- Title, summary, and publication date
- Featured image
- Feed source and category
- Click handler for expanded view

#### `ExpandedArticleView.tsx`
Modal component showing full article:
- Complete article content
- Full-size images
- Original link
- Close button and overlay

#### `FeedManager.tsx`
Feed selection interface:
- List of available RSS feeds
- Toggle feed active/inactive status
- Add new feeds
- Feed status indicators

#### `SearchBar.tsx`
Search interface with:
- Search query input
- Time filter dropdown (24h, 7d, 30d, all)
- Clear button
- Loading states

#### `Pagination.tsx`
Pagination controls:
- Page numbers
- Previous/Next buttons
- Total items count
- Responsive design

### Utility Components

#### `DarkModeToggle.tsx`
Button to toggle dark mode with:
- Sun/Moon icon
- Smooth transitions
- Persistent state

#### `Footer.tsx`
Page footer component (if applicable)

## API Integration

The frontend communicates with the backend through `lib/api.ts`:

### API Client

```typescript
import { newsApi } from '@/lib/api';

// Get articles
const articles = await newsApi.getArticles({
  page: 1,
  per_page: 20,
  feeds: ['TechCrunch', 'BBC News']
});

// Search articles
const results = await newsApi.searchArticles({
  query: 'AI',
  time_filter: '24h',
  page: 1,
  per_page: 20
});

// Get feeds
const feeds = await newsApi.getFeeds();

// Add feed
await newsApi.addFeed({
  name: 'New Feed',
  url: 'https://example.com/feed',
  category: 'Tech'
});
```

### TypeScript Types

```typescript
interface NewsArticle {
  id: number;
  title: string;
  summary?: string;
  content?: string;
  link: string;
  author?: string;
  published_date?: string;
  category: string;
  feed_id?: number;
  image_url?: string;
  slug?: string;
  created_at: string;
  updated_at?: string;
  feed_name?: string;
}

interface RSSFeed {
  id: number;
  name: string;
  url: string;
  category: string;
  description?: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}
```

## State Management

### Local State
- Uses React hooks (`useState`, `useEffect`) for component-level state
- `useSearchParams` for URL state synchronization

### Persistence
- **LocalStorage**: Saves browsing state (page, filters, search)
- **URL Parameters**: Reflects current state in URL for sharing
  - `?page=2` - Current page number
  - `?feeds=TechCrunch,BBC` - Selected feeds
  - `?tab=search` - Search mode
  - `?q=AI` - Search query
  - `?timeFilter=7d` - Time filter

### State Flow
1. Load state from URL on mount
2. User interacts with UI
3. State updates trigger re-renders
4. State saved to localStorage
5. URL updated to reflect state

## Styling

### Tailwind CSS
The project uses Tailwind CSS with custom configuration:

```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: { /* custom colors */ }
      }
    }
  }
}
```

### Dark Mode
Dark mode is implemented using:
- Tailwind's `dark:` prefix for styles
- React Context for theme state
- localStorage for persistence
- CSS variables for smooth transitions

### Responsive Design
- Mobile-first approach
- Breakpoints: `sm` (640px), `md` (768px), `lg` (1024px)
- Grid layouts adapt from 1 to 3 columns
- Touch-friendly buttons and controls

## Environment Variables

### Required Variables

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Optional Variables

```env
# Analytics (if implemented)
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX

# Feature flags (if implemented)
NEXT_PUBLIC_ENABLE_SEARCH=true
NEXT_PUBLIC_ENABLE_FEED_MANAGER=true
```

## Development

### Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint

# Type check
npm run type-check
```

### Code Quality

- **TypeScript**: Strict mode enabled
- **ESLint**: Next.js recommended config
- **Prettier**: Code formatting (if configured)

### Adding a New Component

1. Create component file in `components/`:
```typescript
// components/NewComponent.tsx
interface NewComponentProps {
  // Props definition
}

export default function NewComponent({ }: NewComponentProps) {
  // Component logic
  return (
    <div>
      {/* JSX */}
    </div>
  );
}
```

2. Import and use in parent component:
```typescript
import NewComponent from '@/components/NewComponent';

// Usage
<NewComponent prop1="value" />
```

## Performance Optimization

### Implemented Optimizations
- **Code Splitting**: Automatic with Next.js
- **Image Optimization**: Next.js Image component (when used)
- **Lazy Loading**: Suspense boundaries for async components
- **Debouncing**: State persistence debounced to reduce writes
- **Pagination**: Limits articles per page to reduce initial load

### Potential Improvements
- Implement React Query for better caching
- Add image lazy loading
- Implement virtual scrolling for long lists
- Add service worker for offline support
- Optimize bundle size with dynamic imports

## Deployment

### Vercel (Recommended)
1. Connect repository to Vercel
2. Configure environment variables
3. Deploy automatically on push

### Docker
```bash
# Build image
docker build -t news4u-frontend .

# Run container
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://api.example.com \
  news4u-frontend
```

### Static Export (if applicable)
```bash
npm run build
# Deploy 'out' directory to static hosting
```

## Troubleshooting

### API Connection Errors
```
Error: Network Error
```
**Solution**: Verify `NEXT_PUBLIC_API_URL` is correct and backend is running

### Build Errors
```
Type error: Cannot find module
```
**Solution**: Clear `.next` directory and reinstall dependencies:
```bash
rm -rf .next node_modules
npm install
npm run build
```

### Dark Mode Not Persisting
**Solution**: Check browser localStorage is enabled and not full

### State Not Persisting
**Solution**:
- Check browser console for localStorage errors
- Verify state keys in localStorage
- Clear localStorage and reload: `localStorage.clear()`

## Contributing

When contributing to the frontend:
1. Follow TypeScript best practices
2. Use functional components with hooks
3. Follow existing naming conventions
4. Test on multiple screen sizes
5. Ensure dark mode compatibility
6. Add proper TypeScript types
7. Update this README for significant changes

## Related Documentation

- [Backend API Documentation](../backend/README.md)
- [Backend Quick Start](../backend/QUICKSTART.md)
- [Database Setup](../backend/DATABASE_SETUP.md)
- [Root README](../README.md)
