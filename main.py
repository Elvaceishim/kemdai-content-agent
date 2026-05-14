import os
from dotenv import load_dotenv
from src.agent import run_content_agent
from src.memory import save_memory

load_dotenv()

def main():
    print("=" * 60)
    print("Kemdai Content Strategy Agent")
    print("Persistent memory powered by Supabase + pgvector")
    print("=" * 60)

    while True:
        print("\nWhat would you like to do?")
        print("1. Get content suggestions")
        print("2. Log past content to memory")
        print("3. Exit")

        choice = input("\nEnter choice (1/2/3): ").strip()

        if choice == "1":
            print("\n--- Content Suggestion ---")
            topic = input("Topic or theme: ").strip()
            
            print("\nPlatform:")
            print("1. Twitter/X")
            print("2. LinkedIn")
            print("3. Instagram")
            platform_choice = input("Choose (1/2/3): ").strip()
            platform_map = {"1": "Twitter/X", "2": "LinkedIn", "3": "Instagram"}
            platform = platform_map.get(platform_choice, "Twitter/X")

            print("\nContent type:")
            print("1. Post")
            print("2. Thread")
            print("3. Campaign angle")
            print("4. Story")
            type_choice = input("Choose (1/2/3/4): ").strip()
            type_map = {"1": "post", "2": "thread", "3": "campaign", "4": "story"}
            content_type = type_map.get(type_choice, "post")

            print(f"\n🧠 Checking memory and generating suggestions for '{topic}'...")
            result = run_content_agent(topic, platform, content_type)

            print("\n" + "=" * 60)
            print("CONTENT SUGGESTIONS")
            print("=" * 60)
            print(f"\nMemory context: {result['recent_memory_count']} recent entries, {result['similar_memory_count']} similar entries found")
            print("\n" + result["suggestion"])

            # Ask if they want to save this session to memory
            save = input("\nSave this topic to memory? (y/n): ").strip().lower()
            if save == "y":
                angle = input("What angle did you use/choose? (brief description): ").strip()
                performance = input("Performance (high/medium/low/unknown): ").strip() or "unknown"
                notes = input("Any notes? (press Enter to skip): ").strip()
                
                save_memory(
                    content_type=content_type,
                    platform=platform,
                    topic=topic,
                    angle=angle,
                    performance=performance,
                    notes=notes,
                )
                print("✅ Saved to memory.")

        elif choice == "2":
            print("\n--- Log Past Content to Memory ---")
            content_type = input("Content type (post/thread/campaign/story): ").strip()
            platform = input("Platform (Twitter/X, LinkedIn, Instagram): ").strip()
            topic = input("Topic: ").strip()
            angle = input("Angle used: ").strip()
            performance = input("Performance (high/medium/low/unknown): ").strip() or "unknown"
            notes = input("Notes (press Enter to skip): ").strip()

            save_memory(
                content_type=content_type,
                platform=platform,
                topic=topic,
                angle=angle,
                performance=performance,
                notes=notes,
            )
            print("✅ Logged to memory.")

        elif choice == "3":
            print("\nExiting. Memory persists in Supabase.")
            break

        else:
            print("Invalid choice. Enter 1, 2, or 3.")

if __name__ == "__main__":
    main()