from langchain.vectorstores import FAISS
from langchain.document_loaders import WebBaseLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

URLS = ["https://giki.edu.pk/",
        "https://giki.edu.pk/vision-and-mission/",
        "https://giki.edu.pk/institute/",
        "https://giki.edu.pk/academics/office-of-admission-examination/",
        "https://admissions.giki.edu.pk/Home/Index",
        "https://giki.edu.pk/admissions/admissions-undergraduates/ugradhow-to-apply/",
        "https://giki.edu.pk/admissions/admissions-undergraduates/ugrad-fees-and-expenses/",
        "https://giki.edu.pk/admissions/admissions-undergraduates/",
        "https://giki.edu.pk/contact-us-main/",
        "https://giki.edu.pk/admissions/admissions-undergraduates/",
        "https://giki.edu.pk/admissions/admissions-undergraduates/ugrad-aid-scholarships/",
        "https://giki.edu.pk/admissions/admissions-graduate/",
        "https://giki.edu.pk/admissions/admissions-graduate/grad-aid-scholarships/"
]

loader = WebBaseLoader(URLS)
docs = loader.load()
embeddings = HuggingFaceEmbeddings()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
texts = text_splitter.split_documents(docs)
db = FAISS.from_documents(texts, embeddings)
db.save_local("gikichat_faiss_index")