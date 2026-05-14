import os
from datetime import date
from supabase import create_client, Client
from src.embeddings import get_embedding

def get_supabase() -> Client:
    return create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_SERVICE_KEY")
    )

def save_memory(
    content_type: str,
    platform: str,
    topic: str,
    angle: str,
    performance: str = "unknown",
    notes: str = ""
):
    supabase = get_supabase()
    
    # Create embedding from the combined content context
    text_to_embed = f"{content_type} {platform} {topic} {angle} {notes}"
    embedding = get_embedding(text_to_embed)
    
    record = {
        "content_type": content_type,
        "platform": platform,
        "topic": topic,
        "angle": angle,
        "performance": performance,
        "notes": notes,
        "session_date": date.today().isoformat(),
        "embedding": embedding,
    }
    
    result = supabase.table("content_memory").insert(record).execute()
    return result.data[0] if result.data else None

def get_recent_memories(limit: int = 10) -> list:
    supabase = get_supabase()
    result = (
        supabase.table("content_memory")
        .select("content_type, platform, topic, angle, performance, notes, session_date")
        .order("session_date", desc=True)
        .limit(limit)
        .execute()
    )
    return result.data or []

def get_similar_memories(topic: str, limit: int = 5) -> list:
    supabase = get_supabase()
    embedding = get_embedding(topic)
    
    result = supabase.rpc(
        "match_content_memory",
        {
            "query_embedding": embedding,
            "match_threshold": 0.7,
            "match_count": limit,
        }
    ).execute()
    
    return result.data or []

def format_memories_for_prompt(memories: list) -> str:
    if not memories:
        return "No past content memory found."
    
    lines = []
    for m in memories:
        line = f"- [{m.get('session_date', 'unknown date')}] {m.get('platform', '')} | {m.get('content_type', '')} | Topic: {m.get('topic', '')} | Angle: {m.get('angle', '')} | Performance: {m.get('performance', '')}"
        if m.get('notes'):
            line += f" | Notes: {m['notes']}"
        lines.append(line)
    
    return "\n".join(lines)