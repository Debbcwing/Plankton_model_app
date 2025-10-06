"""
RAG System Configuration
This script processes PDF documents and creates a vector database for retrieval.
"""

import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import streamlit as st


class RAGSystem:
    """RAG system for querying PhD research documents."""

    def __init__(self, data_folder="data", persist_directory="chroma_db"):
        self.data_folder = data_folder
        self.persist_directory = persist_directory
        self.embeddings = None
        self.vectorstore = None

    @st.cache_resource
    def initialize_embeddings(_self):
        """Initialize embedding model (cached to avoid reloading)."""
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
        """Load existing vector database."""
        self.embeddings = self.initialize_embeddings()

        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )

        return self.vectorstore

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
