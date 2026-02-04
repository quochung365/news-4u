import re
import random
import string

def get_or_build_slug(url: str, title: str) -> str:
    """
    Extract slug from URL or generate a new one from title if not present.
        
    Args:
        url: The article URL
        title: The article title (not used in this function)
    Returns:
        The extracted slug
    """
    url_parts = url.split('/')
    slug = ''
    if len(url_parts) == 0:
        slug = generate_slug(title)
    if url_parts[-1] == '':
        slug = url_parts[-2].replace('.html', '')
    else: 
        slug = url_parts[-1].replace('.html', '')

    if slug == '':
        slug = generate_slug(title)

    slug += ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    
    return slug

def generate_slug(title: str) -> str:
    """
    Generate a URL-friendly slug from an article title.
    Format: first 15 characters of title + 8 random alphanumeric characters
    
    Args:
        title: The article title
        article_id: Optional article ID to ensure uniqueness
    
    Returns:
        A URL-friendly slug
    """
    # Clean the title: remove special characters, convert to lowercase
    clean_title = re.sub(r'[^a-zA-Z0-9\s]', '', title.lower())
    
    # Take first 15 characters, remove extra spaces
    title_part = re.sub(r'\s+', '', clean_title)[:15]
    
    # Generate 8 random alphanumeric characters
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    # Combine title part and random part
    slug = f"{title_part}{random_part}"
    
    return slug
