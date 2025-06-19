#!/usr/bin/env python3
"""
Ethics of the Fathers Search System
Search through the teachings for relevant wisdom based on keywords or themes.
"""

import os
import re
from pathlib import Path

class EthicsSearcher:
    def __init__(self, ethics_dir="ethics-of-fathers"):
        self.ethics_dir = Path(ethics_dir)
        self.chapters = {}
        self.load_chapters()
    
    def load_chapters(self):
        """Load all chapter files into memory for searching."""
        for file_path in self.ethics_dir.glob("chapter-*.md"):
            chapter_num = re.search(r'chapter-(\d+)', file_path.name).group(1)
            with open(file_path, 'r', encoding='utf-8') as f:
                self.chapters[chapter_num] = f.read()
    
    def search_by_keyword(self, keyword, context_lines=3):
        """Search for a keyword across all chapters."""
        results = []
        keyword_lower = keyword.lower()
        
        for chapter_num, content in self.chapters.items():
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if keyword_lower in line.lower():
                    # Get context around the match
                    start = max(0, i - context_lines)
                    end = min(len(lines), i + context_lines + 1)
                    context = '\n'.join(lines[start:end])
                    
                    results.append({
                        'chapter': chapter_num,
                        'line_number': i + 1,
                        'context': context,
                        'match_line': line.strip()
                    })
        
        return results
    
    def search_by_theme(self, theme):
        """Search for teachings related to common themes."""
        theme_keywords = {
            'learning': ['learn', 'study', 'torah', 'wisdom', 'teach', 'pupil', 'student'],
            'character': ['character', 'heart', 'good', 'righteous', 'virtue', 'trait'],
            'relationships': ['friend', 'neighbor', 'community', 'peace', 'love', 'kindness'],
            'leadership': ['leader', 'judge', 'government', 'power', 'authority', 'responsibility'],
            'service': ['serve', 'service', 'god', 'divine', 'holy', 'mitzvah'],
            'humility': ['humble', 'humility', 'pride', 'arrogance', 'modest'],
            'justice': ['justice', 'judgment', 'fair', 'righteous', 'law'],
            'work': ['work', 'labor', 'business', 'livelihood', 'occupation'],
            'growth': ['grow', 'growth', 'improve', 'develop', 'increase', 'progress']
        }
        
        if theme.lower() not in theme_keywords:
            return f"Theme '{theme}' not found. Available themes: {', '.join(theme_keywords.keys())}"
        
        all_results = []
        for keyword in theme_keywords[theme.lower()]:
            results = self.search_by_keyword(keyword, context_lines=2)
            all_results.extend(results)
        
        # Remove duplicates and sort by chapter
        unique_results = []
        seen_contexts = set()
        for result in all_results:
            if result['context'] not in seen_contexts:
                unique_results.append(result)
                seen_contexts.add(result['context'])
        
        return sorted(unique_results, key=lambda x: (x['chapter'], x['line_number']))
    
    def get_wisdom_for_question(self, question):
        """Get relevant wisdom for a specific life question."""
        question_patterns = {
            'motivation': ['motivation', 'purpose', 'meaning', 'drive', 'energy'],
            'conflict': ['conflict', 'argument', 'fight', 'disagree', 'anger', 'difficult'],
            'growth': ['grow', 'improve', 'better', 'develop', 'change'],
            'priorities': ['priority', 'important', 'focus', 'overwhelm', 'balance'],
            'relationships': ['relationship', 'friend', 'family', 'love', 'marriage'],
            'work': ['work', 'job', 'career', 'business', 'money'],
            'forgiveness': ['forgive', 'hurt', 'pain', 'resentment', 'anger'],
            'leadership': ['lead', 'manage', 'responsibility', 'authority', 'decision']
        }
        
        question_lower = question.lower()
        relevant_themes = []
        
        for theme, keywords in question_patterns.items():
            if any(keyword in question_lower for keyword in keywords):
                relevant_themes.append(theme)
        
        if not relevant_themes:
            return "I'm not sure which teaching applies to your question. Try searching for specific keywords."
        
        all_results = []
        for theme in relevant_themes:
            if theme in ['motivation', 'growth', 'priorities']:
                results = self.search_by_theme('growth')
            elif theme in ['conflict', 'forgiveness']:
                results = self.search_by_theme('relationships')
            elif theme == 'work':
                results = self.search_by_theme('work')
            elif theme == 'leadership':
                results = self.search_by_theme('leadership')
            else:
                results = self.search_by_theme(theme)
            
            if isinstance(results, list):
                all_results.extend(results)
        
        return all_results[:5]  # Return top 5 most relevant results

def main():
    """Interactive search interface."""
    searcher = EthicsSearcher()
    
    print("=" * 60)
    print("Welcome to the Ethics of the Fathers Search System")
    print("=" * 60)
    print()
    print("Ask me for wisdom! You can:")
    print("1. Search by keyword: 'search [word]'")
    print("2. Search by theme: 'theme [theme]'")
    print("3. Ask a question: 'question [your question]'")
    print("4. Type 'help' for available themes")
    print("5. Type 'quit' to exit")
    print()
    
    while True:
        user_input = input("🕊️  Ask the fathers: ").strip()
        
        if user_input.lower() == 'quit':
            print("\nMay the wisdom of our fathers guide you. Shalom!")
            break
        
        elif user_input.lower() == 'help':
            print("\nAvailable themes:")
            themes = ['learning', 'character', 'relationships', 'leadership', 
                     'service', 'humility', 'justice', 'work', 'growth']
            for theme in themes:
                print(f"  - {theme}")
            print()
        
        elif user_input.lower().startswith('search '):
            keyword = user_input[7:].strip()
            results = searcher.search_by_keyword(keyword)
            print(f"\n📚 Found {len(results)} results for '{keyword}':")
            for result in results[:5]:  # Show top 5
                print(f"\n--- Chapter {result['chapter']} ---")
                print(result['context'])
                print()
        
        elif user_input.lower().startswith('theme '):
            theme = user_input[6:].strip()
            results = searcher.search_by_theme(theme)
            if isinstance(results, str):
                print(f"\n{results}")
            else:
                print(f"\n🎯 Found {len(results)} teachings about '{theme}':")
                for result in results[:5]:  # Show top 5
                    print(f"\n--- Chapter {result['chapter']} ---")
                    print(result['context'])
                    print()
        
        elif user_input.lower().startswith('question '):
            question = user_input[9:].strip()
            results = searcher.get_wisdom_for_question(question)
            if isinstance(results, str):
                print(f"\n{results}")
            else:
                print(f"\n💡 Wisdom for your question:")
                for result in results[:3]:  # Show top 3
                    print(f"\n--- Chapter {result['chapter']} ---")
                    print(result['context'])
                    print()
        
        else:
            # Treat as a general question
            results = searcher.get_wisdom_for_question(user_input)
            if isinstance(results, str):
                print(f"\n{results}")
            else:
                print(f"\n💡 Wisdom for your question:")
                for result in results[:3]:  # Show top 3
                    print(f"\n--- Chapter {result['chapter']} ---")
                    print(result['context'])
                    print()

if __name__ == "__main__":
    main() 