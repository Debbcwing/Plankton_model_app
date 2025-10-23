"""
RAG System Configuration
This script processes PDF documents and creates a vector database for retrieval.

Setup:
- Local embeddings using sentence-transformers (free, runs on CPU)
- Claude (Anthropic) for answering questions (configured in app.py)
"""

import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class RAGSystem:
    """RAG system for querying PhD research documents."""

    def __init__(self, data_folder="data", persist_directory="chroma_db"):
        self.data_folder = data_folder
        self.persist_directory = persist_directory
        self.embeddings = None
        self.vectorstore = None

    def initialize_embeddings(self):
        """Initialize local embedding model (lightweight, CPU-friendly)."""
        print("✓ Using local embeddings (all-MiniLM-L6-v2)")

        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )

    def load_and_process_pdfs(self):
        """Load PDFs from data folder and split into chunks."""
        documents = []
        pdf_files = list(Path(self.data_folder).glob("*.pdf"))

        print(f"Found {len(pdf_files)} PDF files to process...")

        for pdf_path in pdf_files:
            print(f"Processing: {pdf_path.name}")
            loader = PyPDFLoader(str(pdf_path))
            docs = loader.load()
            documents.extend(docs)

        # Split documents into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,  # Characters per chunk
            chunk_overlap=300,  # Overlap between chunks
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

        chunks = text_splitter.split_documents(documents)

        # Filter out very short chunks (likely headers/footers with no content)
        filtered_chunks = [chunk for chunk in chunks if len(chunk.page_content.strip()) > 200]
        print(f"Created {len(filtered_chunks)} text chunks from {len(documents)} pages (filtered from {len(chunks)} total)")

        return filtered_chunks

    def create_vectorstore(self, chunks):
        """Create and persist vector database from document chunks."""
        self.embeddings = self.initialize_embeddings()

        print("Creating vector database...")
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )

        print(f"Vector database created and saved to {self.persist_directory}")
        return self.vectorstore

    def load_vectorstore(self):
        """Load existing vector database with validation."""
        self.embeddings = self.initialize_embeddings()

        try:
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )

            # Validate that the database has content
            try:
                collection = self.vectorstore._collection
                doc_count = collection.count()

                if doc_count == 0:
                    raise ValueError("Vector database is empty")

                print(f"✓ Loaded vector database with {doc_count} documents")

            except Exception as e:
                print(f"Warning: Could not validate database content: {e}")
                # Continue anyway - let it fail later if truly broken

            return self.vectorstore

        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error loading vector database: {error_msg}")

            # Check for specific database errors
            if "no such table" in error_msg.lower() or "acquire_write" in error_msg.lower():
                raise ValueError(
                    "Database error: ChromaDB version mismatch or corrupted database. "
                    "Please rebuild by running: python rebuild_chroma_db.py"
                )
            elif "Embeddings" in error_msg or "empty" in error_msg.lower():
                raise ValueError(
                    "Vector database is corrupted or empty. "
                    "Please rebuild by running: python rebuild_chroma_db.py"
                )
            else:
                raise ValueError(
                    f"Failed to load vector database: {error_msg}. "
                    f"Try rebuilding with: python rebuild_chroma_db.py"
                )

    def setup(self, force_rebuild=False):
        """
        Setup RAG system - create or load vector database.

        Args:
            force_rebuild: If True, rebuild database even if it exists
        """
        if force_rebuild or not os.path.exists(self.persist_directory):
            print("Building new vector database...")
            chunks = self.load_and_process_pdfs()
            self.create_vectorstore(chunks)
        else:
            print("Loading existing vector database...")
            self.load_vectorstore()

        return self.vectorstore


def main():
    """Run this script to build/rebuild the vector database."""
    print("=== RAG System Setup ===")
    rag = RAGSystem()

    # Ask user if they want to rebuild
    rebuild = input("Rebuild vector database? (y/n): ").lower() == 'y'

    rag.setup(force_rebuild=rebuild)
    print("\n✓ RAG system ready!")
    print(f"✓ Vector database stored in: {rag.persist_directory}")


if __name__ == "__main__":
    main()
