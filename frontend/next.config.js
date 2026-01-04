/** @type {import('next').NextConfig} */
const nextConfig = {
  // Memory optimization
  swcMinify: true,
  // Enable standalone output for Docker
  output: 'standalone',
  generateEtags: false,
  // Base path for serving under /news
  // Set via NEXT_PUBLIC_BASE_PATH environment variable, defaults to empty (root)
  basePath: '/news'
};

module.exports = nextConfig; 