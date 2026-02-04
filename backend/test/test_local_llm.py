# summarize it in 30-100 words (you can use bullet points if needed, but prioritize non-bullet points). Try to make it as concise as possible
import trafilatura
import ollama
import time

def get_summary(url):
    # Step 1: Extract content using trafilatura
    downloaded = trafilatura.fetch_url(url)
    article_title = 'Here are the 55 US AI startups that have raised $100M or more in 2025!'
    article_text = trafilatura.extract(downloaded)

    if not article_text:
        return "Could not extract text from the provided URL."

    # Step 2: Feed the content to Gemma via Ollama
    # We use a 'system' role to set the persona and 'user' for the content
    start_time = time.time()
    response = ollama.chat(model='gemma2:2b', messages=[
        {
            'role': 'system',
            'content': 'You are a professional news editor. Summarize the following article, usse bullet points if needed (prefer non-bullet points if possible). Focus on key facts and ignore ads. Keep it short and concise. Maximum 100 words.',
        },
        {
            'role': 'user',
            'content': f"ARTICLE TITLE:\n{article_title}\n\n ARTICLE CONTENT:\n{article_text}",
        },
    ])
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")

    return response['message']['content'], end_time - start_time

if __name__ == "__main__":
    input_url = input("Enter the URL of the article: ")
    summary, time_taken = get_summary(input_url)
    print(summary)
    print(f"Time taken: {time_taken} seconds")