"""
Quick Test Script for Phase 1 Features
Tests all new modules without voice input
"""

print("=" * 60)
print("TESTING PHASE 1 FEATURES")
print("=" * 60)

# Test imports
try:
    print("\n1. Testing imports...")
    from skills.file_manager import search_files, list_directory
    from skills.web_search import wikipedia_query, define_word
    from skills.reminders import create_note, list_notes
    from skills.screen_tools import get_clipboard_text
    print("✅ All modules imported successfully!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Run: pip install requests beautifulsoup4 pyperclip win10toast schedule")
    exit(1)

# Test File Manager
print("\n2. Testing File Manager...")
try:
    result = list_directory(".")
    print(f"✅ Directory listing: {len(result)} chars returned")
except Exception as e:
    print(f"❌ Error: {e}")

# Test Web Search
print("\n3. Testing Web Search...")
try:
    result = define_word("test")
    print(f"✅ Dictionary lookup: {result[:100]}...")
except Exception as e:
    print(f"⚠️ Web search error (might be network): {e}")

# Test Reminders/Notes
print("\n4. Testing Notes System...")
try:
    result = create_note("test_note", "This is a test note created by the verification script.")
    print(f"✅ Note created: {result}")
    result = list_notes()
    print(f"✅ Notes list: {result[:100]}...")
except Exception as e:
    print(f"❌ Error: {e}")

# Test Clipboard
print("\n5. Testing Clipboard...")
try:
    result = get_clipboard_text()
    print(f"✅ Clipboard access: {result[:100]}..." if result else "✅ Clipboard is empty")
except Exception as e:
    print(f"⚠️ Clipboard error: {e}")

# Test Brain Integration
print("\n6. Testing AI Brain Integration...")
try:
    from core.brain import think
    
    # Test with a simple command
    result = think("what time is it")
    print(f"✅ Brain responded: {result}")
    
    # Test with new feature
    result = think("create a note called ai_test with content: testing ai integration")
    print(f"✅ Brain new feature: {result}")
    
except Exception as e:
    print(f"❌ Brain error: {e}")
    print("Make sure GROQ_API_KEY is set in .env file")

print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print("✅ If you see green checkmarks above, Phase 1 is working!")
print("⚠️ Yellow warnings are okay (network issues)")
print("❌ Red X marks need attention")
print("\nNext step: Run 'python main.py' to test with voice commands")
print("=" * 60)
