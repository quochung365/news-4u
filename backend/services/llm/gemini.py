"""
Gemini LLM service for summarizing news article content.
"""
import logging
from typing import Optional
from google import genai
from google.genai import types
from config.settings import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a professional news summarizer. Your task is to create concise, informative summaries of news articles.

Guidelines:
- Focus on key facts, main points, and important details
- Use clear, straightforward language
- Maximum 100 words
- Use bullet points ONLY when there are multiple distinct important points
- Ignore ads, promotional content, and irrelevant information
- Keep the summary objective and factual"""


class GeminiLLM:
    """Gemini LLM service for article summarization using the free tier."""

    def __init__(self):
        """Initialize Gemini client."""
        self.api_key = settings.GEMINI_API_KEY
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.0-flash-exp"  # Free tier model
        logger.info(f"Initialized GeminiLLM with model: {self.model}")

    def summarize_article(self, title: str, content: str) -> Optional[str]:
        """
        Summarize a single article using Gemini API.

        Args:
            title: Article title
            content: Article content (can be HTML or text)

        Returns:
            Summary string or None if summarization fails
        """
        if not content or not content.strip():
            logger.warning("Empty content provided for summarization")
            return None

        # Clean content (remove HTML tags if present)
        from bs4 import BeautifulSoup
        clean_content = BeautifulSoup(content, 'html.parser').get_text()
        clean_content = ' '.join(clean_content.split())  # Remove extra whitespace

        # Limit content length to avoid hitting token limits (free tier)
        max_content_length = 10000  # ~2500 tokens
        if len(clean_content) > max_content_length:
            clean_content = clean_content[:max_content_length] + "..."
            logger.info("Content truncated to fit token limits")

        prompt = f"""Title: {title}

Content:
{clean_content}

Please provide a concise summary following the guidelines."""

        try:
            logger.info(f"Sending summarization request for article: {title[:50]}...")

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.3,  # Lower temperature for more focused output
                    max_output_tokens=150,  # Roughly 100 words
                )
            )

            if response and response.text:
                summary = response.text.strip()
                logger.info(f"Successfully generated summary ({len(summary)} chars)")
                return summary
            else:
                logger.warning("Empty response from Gemini API")
                return None

        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            return None

    def summarize_batch(self, articles: list[dict]) -> dict[int, str]:
        """
        Summarize multiple articles in batch.

        Args:
            articles: List of dicts with 'id', 'title', and 'content'

        Returns:
            Dictionary mapping article_id to summary
        """
        results = {}

        for article in articles:
            article_id = article.get('id')
            title = article.get('title', '')
            content = article.get('content', '')

            if not article_id:
                logger.warning("Article without ID, skipping")
                continue

            summary = self.summarize_article(title, content)
            if summary:
                results[article_id] = summary

        logger.info(f"Batch summarization complete: {len(results)}/{len(articles)} successful")
        return results


# Global instance
gemini_llm = GeminiLLM()
