/** @type {import('next').NextConfig} */
const nextConfig = {

  swcMinify: true, // Memory optimization
  output: 'standalone', // For Docker deployment
  generateEtags: false,  // Disable etags for better performance
};

module.exports = nextConfig; 