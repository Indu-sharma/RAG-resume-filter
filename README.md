# Simple resume filter RAG 🎯📄🚀

---

## 📝 **Problem Summary**

Is your inbox flooded with resumes? 📥 No worries! This project (sample learning poc project) helps you easily filter, shortlist, and analyze resumes for specific job requirements.

- **Upload Resumes Once**: Batch upload all your resumes.
- **Query Anytime**: Perform multiple queries on aggregated data.
- **Powerful Search**: Leverage GPT models to extract candidate details.

Get started today with resume filtering made simple! 🚀
---

## 📊 **RAG Flow**

The following diagram illustrates the **Retrieval-Augmented Generation** process used in this project:

![RAG](RAG.JPEG)

---

## 🛠️ **Main Pipeline**

The pipeline includes the following key steps:
1. **Load Documents** (Resumes)
2. **Create Nodes** from the Resumes
3. **Build an Index** for efficient searching
4. **Initialize the Query Engine**
5. **Query the Index** using user prompts
6. **Generate Response** using retrieved nodes

The system allows users to upload multiple resumes and query them based on specific job requirements, skill sets, and experience.

---

## ⚙️ **Installation and Setup**

Follow these simple steps to set up the project locally:

### 1. Clone the repository 🖥️
git clone https://github.com/your-username/resume-filter-rag.git
cd resume-filter-rag

### 2. Create and activate virtaul env 
- or use poetry or other dependency managers 
### 3. Install dependencies 📦
pip install -r requirements.txt
### 5. Configure OpenAI Key 🔑
Update your .env file in the root directory with your OpenAI API key:
LLM_API_KEY=your_openai_api_key
### 6. Start the server 
python -m  backend.main  
### 7. Upload Resumes 📤
Place all your resumes in the resumes/ directory.

Note: Upload all resumes at once. For incremental uploads, new resumes will be aggregated with the existing ones.

## 💡 How to Use

- In search section enter questions/ Job description. Example- "Who has the best experience for Python API development?"

- Response:
Hello, I am here to help with resume selection for Python API development. Based on the information provided, here is a candidate who matches the skills for Python API development:
- **Candidate Name**: R***** ***** (Masked for privacy)
- **Skill Match Percentage**: 90%
- **Experience**: Teaching Assistant at A**** Academy By Interview Bit

## 🌟 Next Steps
- Fine Tune, retrain, test RAG pipeline for better results in candidate matching. 
- Explore deeper into LlamaIndex, Embedding/Vector stores. 
- Explore latest openapi models such as gpt4o for generation so that search results are better. 
