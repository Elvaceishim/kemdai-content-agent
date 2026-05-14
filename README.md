# Kemdai Content Strategy Agent

A content strategy agent with persistent episodic memory, built for the Kemdai brand. The agent remembers past content campaigns, tracks what angles have been used and how they performed, and uses that memory to suggest genuinely fresh content ideas — avoiding repetition and building on what works.

Built as part of a deliberate AI engineering skill-building track targeting production agentic systems roles.

---

## What it does

- Accepts a content topic, platform, and content type as input
- Pulls recent content history and semantically similar past entries from Supabase
- Injects that memory into the agent's context as reasoning material
- Suggests 3 fresh angles that haven't been recently used, with strategic priority ratings
- Recommends one angle to execute first with an exact opening line
- Saves every session to persistent vector memory for future reference
- Memory compounds over time — the more you use it, the smarter it gets

---

## Why it matters

Most AI content tools have zero memory. Every session starts blank, generating the same generic ideas regardless of what's already been posted. This agent maintains an episodic memory layer — it knows what was suggested last week, what the audience responded to, and what to avoid. That's the production-relevant pattern behind enterprise content intelligence systems.

---

## Architecture

User input (topic + platform + content type)
↓
Memory retrieval (recent + semantic similarity via pgvector)
↓
Context injection into agent prompt
↓
Claude 3.5 Haiku reasons about memory + generates fresh angles
↓
User selects angle → saved back to memory with embedding
↓
Memory grows, future suggestions improve

---

## Stack

| Layer             | Technology                                   |
| ----------------- | -------------------------------------------- |
| Agent LLM         | Claude 3.5 Haiku via OpenRouter              |
| Vector Memory     | Supabase + pgvector                          |
| Embeddings        | OpenAI text-embedding-3-small via OpenRouter |
| Similarity Search | Cosine similarity with 0.7 threshold         |
| Runtime           | Python 3.12                                  |

---

## Running locally

```bash
git clone https://github.com/Elvaceishim/kemdai-content-agent.git
cd kemdai-content-agent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run the agent:

```bash
python main.py
```

---

## Database schema

```sql
create table content_memory (
    id uuid default gen_random_uuid() primary key,
    created_at timestamp with time zone default now(),
    session_date date default current_date,
    content_type text not null,
    platform text not null,
    topic text not null,
    angle text not null,
    performance text,
    notes text,
    embedding vector(1536)
);
```

Vector similarity search is handled by a Supabase RPC function `match_content_memory` using cosine distance.

---

## Example session

Topic: freelancer payment safety
Platform: Twitter/X
Content type: post
Memory context: 3 recent entries, 0 similar entries found
Suggested angles:

"The Cost of Ghosting" — macro economic narrative [HIGH priority]
"Freelance Dignity" — reframing upfront payment as professional [MEDIUM priority]
"Your Skills Have a Price Tag" — numbers-driven economics [HIGH priority]

Recommended: Angle 1
Opening line: "Every unpaid invoice is a Nigerian talent lost. Here's how payment
uncertainty is bleeding our creative economy dry."

---

## Project structure

kemdai-content-agent/
├── src/
│ ├── agent.py # Agent logic + memory-aware prompt construction
│ ├── memory.py # Supabase read/write + vector similarity search
│ ├── embeddings.py # OpenRouter embedding generation
│ └── init.py
├── main.py # CLI interface
├── .env # API keys (not committed)
└── requirements.txt

---

## Author

**Elvis Anselm** — AI Engineer & Content Strategist, Lagos Nigeria
[Portfolio](https://elvace.netlify.app) · [LinkedIn](https://www.linkedin.com/in/elvisanselm/) · [GitHub](https://github.com/Elvaceishim) · [Repository](https://github.com/Elvaceishim/kemdai-content-agent)
