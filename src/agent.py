import os
from openai import OpenAI
from src.memory import (
    get_recent_memories,
    get_similar_memories,
    format_memories_for_prompt,
    save_memory,
)

def run_content_agent(topic: str, platform: str, content_type: str) -> dict:
    client = OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    )

    # Pull recent memories and similar past content
    recent = get_recent_memories(limit=10)
    similar = get_similar_memories(topic, limit=5)

    recent_context = format_memories_for_prompt(recent)
    similar_context = format_memories_for_prompt(similar)

    system_prompt = """You are a content strategy agent for Kemdai — a freelancer payment escrow platform for the Nigerian market. 
Your tagline is: "Your payment is safe. Your work is paid."

Your job is to suggest fresh, non-repetitive content ideas for the Kemdai brand.

You have access to past content memory — what has been posted before, what angles have been used, and how content performed. 
Use this memory to:
1. Avoid repeating angles that were recently used
2. Build on angles that performed well
3. Suggest genuinely fresh perspectives that haven't been explored yet

Your target audience is Nigerian freelancers and their clients — designers, developers, writers, photographers, and the businesses that hire them.

Always be direct, specific, and actionable. No generic advice."""

    user_prompt = f"""I need content ideas for Kemdai.

Platform: {platform}
Content type: {content_type}
Topic/theme: {topic}

--- RECENT CONTENT HISTORY (last 10 entries) ---
{recent_context}

--- SIMILAR PAST CONTENT (semantically related) ---
{similar_context}

Based on this memory, suggest 3 fresh content angles I haven't used recently. For each angle:
1. Give it a specific headline or hook
2. Explain the angle in 2-3 sentences
3. Note why this is fresh given the past content history
4. Rate the strategic priority: High / Medium / Low

Then recommend which ONE angle to execute first and why.

Finally, suggest the exact opening line for that content piece."""

    response = client.chat.completions.create(
        model="anthropic/claude-3.5-haiku",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.8,
    )

    suggestion = response.choices[0].message.content

    return {
        "topic": topic,
        "platform": platform,
        "content_type": content_type,
        "suggestion": suggestion,
        "recent_memory_count": len(recent),
        "similar_memory_count": len(similar),
    }