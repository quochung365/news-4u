# export GEMINI_API_KEY=AIzaSyAni5WtbT0IfcRJXQ9q1argzG6nRLW7lfQ


from operator import contains
from google import genai

client = genai.Client(api_key="AIzaSyAni5WtbT0IfcRJXQ9q1argzG6nRLW7lfQ")
context='''
Summarize the following article, use bullet points if must be. Focus on key facts and ignore ads. Keep it short and concise. Maximum 100 words.
MAIN_CONTENT
It took Rebecca Yu seven days to vibe code her dining app. She was tired of the decision fatigue that comes from people in a group chat not being able to decide where to eat.
Armed with determination, Claude, and ChatGPT, Yu decided to just build a dining app from scratch — one that would recommend restaurants to her and her friends based on their shared interests.
“Once vibe-coding apps emerged, I started hearing about people with no tech backgrounds successfully building their own apps,” she told TechCrunch. “When I had a week off before school started, I decided it was the perfect time to finally build my application.”
So, she created the web app Where2Eat to help her and her friends find a place to eat.
Yu is part of the growing trend of people who, due to rapid advancements in AI technology, can easily build their own apps for personal use. Most are coding web applications, though they are also increasingly vibe coding mobile apps intended to run only on their own personal phones and devices. Some who are already registered as Apple developers are leaving their personal apps in beta on TestFlight.
It is a new era of app creation that is sometimes called micro apps, personal apps, or fleeting apps because they are intended to be used only by the creator (or the creator plus a select few other people) and only for as long as the creator wants to keep the app. They are not intended for wide distribution or sale.
For example, founder Jordi Amat told TechCrunch that he built a fleeting web gaming app for his family to play over the holidays and simply shut it down once the vacation was over.
Join the Disrupt 2026 Waitlist
Add yourself to the Disrupt 2026 waitlist to be first in line when Early Bird tickets drop. Past Disrupts have brought Google Cloud, Netflix, Microsoft, Box, Phia, a16z, ElevenLabs, Wayve, Hugging Face, Elad Gil, and Vinod Khosla to the stages — part of 250+ industry leaders driving 200+ sessions built to fuel your growth and sharpen your edge. Plus, meet the hundreds of startups innovating across every sector.
Join the Disrupt 2026 Waitlist
Add yourself to the Disrupt 2026 waitlist to be first in line when Early Bird tickets drop. Past Disrupts have brought Google Cloud, Netflix, Microsoft, Box, Phia, a16z, ElevenLabs, Wayve, Hugging Face, Elad Gil, and Vinod Khosla to the stages — part of 250+ industry leaders driving 200+ sessions built to fuel your growth and sharpen your edge. Plus, meet the hundreds of startups innovating across every sector.
Then there’s Shamillah Bankiya, a partner at Dawn Capital, who is building a podcast translation web app for personal use. Interestingly enough, Darrell Etherington, a former TechCrunch writer, now a vice president at SBS Comms, is also building his own personal podcast translation app. “A lot of people I know are using Claude Code, Replit, Bolt, and Lovable to build apps for specific use cases,” he said.
One artist told TechCrunch that he built a “vice tracker” for himself to see how many hookahs and drinks he was consuming each weekend.
Even professional developers are vibe coding personal apps. Software engineer James Waugh told TechCrunch he built a web app planning tool to help with his cooking hobby.
Web apps and mobile
Because tools ranging from Claude Code to Lovable typically don’t require robust coding knowledge just to get to a functional app, we are witnessing the early rise of micro apps. These are apps that are extremely context-specific, address niche needs, and then “disappear when the need is no longer present,” Legand L. Burge III, a professor of computer science at Howard University, said.
“It’s similar to how trends on social media appear and then fade away,” Burge III continued. “But now, [it’s] software itself.”
Yu said she now has six more ideas she wants to code. “It’s really exciting to be alive right now,” she said.
In some ways, it was always easy for someone without much coding experience to create web apps via no-code platforms like Bubble and Adalo, which launched before LLMs became popular. What’s new is the rising ability to create personal, temporary apps for mobile devices, too. Also new: the growing realization that anyone can code just by describing, in regular language, the app they want.
Mobile micro apps still aren’t as easy as their web counterparts. This is because the standard way to load an app on an iPhone is to download it from the App Store, which requires a paid Apple Developer account. But increasingly mobile vibe-coding startups like Anything (which raised $11 million, led by Footwork) and VibeCode (which raised a $9.4 million seed round from Seven Seven Six last year) have emerged to help people build mobile apps.
Christina Melas-Kyriazi, a partner at Bain Capital Ventures, compared this era of app building to social media and Shopify, “where all of a sudden it was really easy to create content or to create a store online, and then we saw an explosion of small sellers.” she said.
Good enough for one
Still, micro apps also have issues. Building and sharing the code with other people can become somewhat expensive given the subscriptions required, especially if all the costs are associated with just one app. Building an app also remains tedious for some. Yu, for example, said her dining app wasn’t hard to create; it was just very time-consuming. She had to lean on ChatGPT and Claude to help her understand some coding decisions. “Once I learned how to prompt and solve issues efficiently, building became much easier,” she said.
Then there are quality issues. Such personal apps may have bugs or critical security flaws — they can’t just be sold as-is to the masses.
But there is still significant potential in an era of personal app building, especially as AI and model reasoning, quality, and security become more sophisticated over time.
The software engineer, Waugh, said he once built an app for a friend who had heart palpitations. He built her a logger that let her record when she was having heart issues so she could more easily show her doctor. “Great example of a one-off personal software that helps you keep track of something important,” he told TechCrunch.
Another founder, Nick Simpson, told TechCrunch he was so bad at paying parking tickets — the consequence of San Francisco’s tough parking availability — that he decided to build an app that would automatically pay them after scanning the ticket. As a registered Apple developer, his app is in beta on TestFlight, but he said a bunch of his friends now want it, too.
Nevertheless, Burge III believes that these types of apps can open “exhilarating opportunities” for businesses and creators to create “hyper-personalized situational experiences.”
Etherington added to that, saying he believes a day is dawning when people stop subscribing to apps that have monthly fees. Instead, they will just build their own apps for personal use.
Melas-Kyriazi, meanwhile, expects to see the use of personal, fleeting apps the same way spreadsheets like Google Sheets or Excel were once used.
“It’s really going to fill the gap between the spreadsheet and a full-fledged product,” she said.
One media strategist, Hollie Krause, said she didn’t like the apps her doctor kept recommending, so she built one herself that can help her track her allergies.
She had no technical experience and finished the web app in the same time it took her husband to go to dinner and back. Now, she said, they have two web apps, both built with Claude: one for allergies and sensitivities, and the other to keep tabs on chores around the house.
“I was like ‘wow I hate Excel but I’d love to make an app for our household,” Krause told TechCrunch. “So, I spun it up and hosted it on Tiiny.host and popped it on our cellphones.”
She thinks vibe coding will bring “a lot of innovation and problem solving for communities that wouldn’t have access otherwise,” and hopes to beta-test her allergy health app so she can one day release it to others.
“The app will be to help others who struggle to navigate life for themselves, and for caregivers to also be able to have access,” she said. “I truly think that vibe coding means I can help people.”

'''
response = client.models.generate_content(model="gemini-3-flash-preview", contents=context)
print(response.text)
with open('./gemini_output', 'w+') as f:
    f.write(response.text)