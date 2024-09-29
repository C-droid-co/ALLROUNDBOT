import requests

NEWS_API_KEY = 'YOUR_NEWS_API_KEY'  # Replace with your NewsAPI.org API key

@client.on(events.NewMessage(pattern='/news'))
async def news(event):
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        if articles:
            news_info = "Top News Headlines:\n"
            for article in articles[:5]:  # Get top 5 articles
                title = article['title']
                url = article['url']
                news_info += f"- {title} ({url})\n"
            await event.respond(news_info)
        else:
            await event.respond("No news articles found.")
    else:
        await event.respond("Failed to fetch news. Please try again later.")
