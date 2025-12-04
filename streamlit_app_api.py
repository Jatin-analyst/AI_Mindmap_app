"""
Streamlit Frontend for PDF Mind Map Generator
Interactive, colorful web interface for generating mind maps from PDFs.
"""
import streamlit as st
import requests
import json
from datetime import datetime
import base64
import os

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(
    page_title="PDF Mind Map Generator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for colorful, interactive UI
st.markdown("""
<style>
    /* Main background gradient */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(90deg, #4A90E2 0%, #7B68EE 100%);
        color: white;
        border-radius: 20px;
        padding: 10px 30px;
        font-weight: bold;
        transition: transform 0.2s;
        border: none;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    /* File uploader styling */
    .uploadedFile {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 10px;
    }
    
    /* Text input styling */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #4A90E2;
    }
    
    /* Success message styling */
    .stSuccess {
        background-color: #51CF66;
        color: white;
        border-radius: 10px;
        padding: 10px;
    }
    
    /* Error message styling */
    .stError {
        background-color: #FF6B6B;
        color: white;
        border-radius: 10px;
        padding: 10px;
    }
    
    /* Header styling */
    h1 {
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    h2, h3 {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "topics" not in st.session_state:
    st.session_state.topics = []
if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = ""
if "mindmap" not in st.session_state:
    st.session_state.mindmap = None
if "topic_name" not in st.session_state:
    st.session_state.topic_name = ""
if "uploaded_file_content" not in st.session_state:
    st.session_state.uploaded_file_content = None

# App title with emoji
st.title("🧠 PDF Mind Map Generator")
st.markdown("### Transform your PDFs into beautiful, interactive mind maps!")

# File upload section
st.markdown("## 📄 Upload Your PDF")
uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type="pdf",
    help="Upload a PDF document to analyze (max 80MB)",
    label_visibility="collapsed"
)

if uploaded_file:
    # Show file info
    file_size_mb = uploaded_file.size / (1024 * 1024)
    st.success(f"✅ Uploaded: {uploaded_file.name} ({file_size_mb:.1f} MB)")
    
    # Store file content in session state
    st.session_state.uploaded_file_content = uploaded_file.getvalue()
    
    # Topic detection section
    st.markdown("## 🔍 Detect Topics")
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("🔍 Detect Topics", key="detect", use_container_width=True):
            with st.spinner("🔄 Analyzing your PDF..."):
                try:
                    # Prepare file for API
                    files = {"file": (uploaded_file.name, st.session_state.uploaded_file_content, "application/pdf")}
                    
                    # Call API
                    response = requests.post(f"{API_URL}/pdf/topics", files=files)
                    
                    if response.ok:
                        data = response.json()
                        st.session_state.topics = data.get("topics", [])
                        st.success(f"✅ Found {len(st.session_state.topics)} topics!")
                    else:
                        error_data = response.json()
                        st.error(f"❌ Error: {error_data.get('detail', {}).get('message', 'Unknown error')}")
                        
                except Exception as e:
                    st.error(f"❌ Error connecting to API: {str(e)}")
    
    # Display detected topics as interactive buttons
    if st.session_state.topics:
        st.markdown("### 💡 Detected Topics (click to select)")
        
        # Create columns for topic buttons
        num_cols = 3
        cols = st.columns(num_cols)
        
        for idx, topic in enumerate(st.session_state.topics):
            with cols[idx % num_cols]:
                if st.button(topic, key=f"topic_{idx}", use_container_width=True):
                    st.session_state.selected_topic = topic
                    st.rerun()
    
    # Topic input section
    st.markdown("## 🎯 Choose Your Topic")
    topic = st.text_input(
        "Enter a topic or select from detected topics above",
        value=st.session_state.selected_topic,
        placeholder="e.g., Machine Learning, Photosynthesis, History...",
        label_visibility="collapsed"
    )
    
    # Generate mind map section
    if topic:
        if st.button("🚀 Generate Mind Map", key="generate", use_container_width=False):
            with st.spinner("🎨 Creating your mind map..."):
                try:
                    # Prepare file and data for API
                    files = {"file": (uploaded_file.name, st.session_state.uploaded_file_content, "application/pdf")}
                    data = {"topic": topic}
                    
                    # Call API
                    response = requests.post(f"{API_URL}/pdf/mindmap", files=files, data=data)
                    
                    if response.ok:
                        result = response.json()
                        st.session_state.mindmap = result.get("mindmap")
                        st.session_state.topic_name = topic
                        st.success(" Mind map generated successfully!")
                    else:
                        error_data = response.json()
                        st.error(f" Error: {error_data.get('detail', {}).get('message', 'Unknown error')}")
                        
                except Exception as e:
                    st.error(f" Error connecting to API: {str(e)}")

# Display mind map section
if st.session_state.mindmap:
    st.markdown("##  Your Interactive Mind Map")
    
    mindmap = st.session_state.mindmap
    
    # Display mind map as JSON (simple visualization)
    st.markdown(f"**Topic:** {mindmap.get('topic', 'N/A')}")
    st.markdown(f"**Number of Nodes:** {len(mindmap.get('nodes', []))}")
    
    # Display nodes in a structured way
    with st.expander(" View Mind Map Structure", expanded=True):
        # Group nodes by parent
        nodes_by_parent = {}
        for node in mindmap.get("nodes", []):
            parent = node["parent"]
            if parent not in nodes_by_parent:
                nodes_by_parent[parent] = []
            nodes_by_parent[parent].append(node)
        
        # Display root nodes (parent = 0)
        if 0 in nodes_by_parent:
            for node in nodes_by_parent[0]:
                st.markdown(f"### 🔹 {node['text']}")
                # Display children
                if node["id"] in nodes_by_parent:
                    for child in nodes_by_parent[node["id"]]:
                        st.markdown(f"  - {child['text']}")
                        # Display grandchildren
                        if child["id"] in nodes_by_parent:
                            for grandchild in nodes_by_parent[child["id"]]:
                                st.markdown(f"    - {grandchild['text']}")
    
    # Download buttons
    st.markdown("##  Download Your Mind Map")
    col1, col2 = st.columns(2)
    
    with col1:
        # JSON download
        json_str = json.dumps(mindmap, indent=2)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{st.session_state.topic_name.replace(' ', '_')}_{timestamp}.json"
        
        st.download_button(
            label=" Download JSON",
            data=json_str,
            file_name=filename,
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        # PNG download placeholder
        st.button(
            " Download PNG",
            help="Image export coming soon!",
            use_container_width=True,
            disabled=True
        )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: white;'>
        <p>Made with passion for college students | Powered by AI (Llama 3)</p>
    </div>
    """,
    unsafe_allow_html=True
)
