#!/usr/bin/env python3
"""
Rebuild ChromaDB vector database for deployment.
This script ensures the database is compatible with the deployed environment.

Run this script to rebuild the database before committing:
    python rebuild_chroma_db.py
"""

import os
import shutil
from pathlib import Path

def main():
    # Import here to avoid import errors if dependencies not installed
    from config.rag_setup import RAGSystem

    db_path = "chroma_db"

    print("=" * 60)
    print("ChromaDB Rebuild Script for Deployment")
    print("=" * 60)

    # Check if database exists
    if os.path.exists(db_path):
        print(f"\n⚠️  Existing database found at: {db_path}")
        response = input("Delete existing database and rebuild? (yes/no): ")

        if response.lower() != 'yes':
            print("❌ Cancelled. Database not modified.")
            return

        # Delete existing database
        print(f"🗑️  Deleting: {db_path}")
        shutil.rmtree(db_path)
        print("✓ Old database deleted")

    # Rebuild database
    print("\n🔨 Building new vector database...")
    print("-" * 60)

    rag = RAGSystem(persist_directory=db_path)
    rag.setup(force_rebuild=True)

    print("-" * 60)
    print("\n✅ Database rebuilt successfully!")
    print(f"📊 Database location: {db_path}")
    print(f"📁 Database size: {get_folder_size(db_path):.2f} MB")

    print("\n" + "=" * 60)
    print("Next Steps:")
    print("=" * 60)
    print("1. Test locally: streamlit run app.py")
    print("2. Commit changes: git add chroma_db/ && git commit -m 'Rebuild vector database'")
    print("3. Push to deployment: git push")
    print("=" * 60)

def get_folder_size(folder_path):
    """Get folder size in MB."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size / (1024 * 1024)

if __name__ == "__main__":
    main()
