"use client";
import React, { useState, useEffect } from 'react';

type KnowledgeDocument = {
  id: string;
  title: string;
  created_at: string;
};

export default function SettingsPage() {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState("");
  const [documents, setDocuments] = useState<KnowledgeDocument[]>([]);

  const fetchDocuments = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/knowledge/');
      if (res.ok) {
        const data = await res.json();
        setDocuments(data.documents);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to delete this document? The AI will forget this information.")) return;
    
    try {
      const res = await fetch(`http://localhost:8000/api/v1/knowledge/${id}`, {
        method: 'DELETE',
      });
      if (res.ok) {
        fetchDocuments();
      } else {
        alert("Failed to delete document.");
      }
    } catch (e) {
      console.error(e);
      alert("Error deleting document.");
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setUploadStatus('idle');
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsUploading(true);
    setUploadStatus('idle');
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/api/v1/knowledge/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Upload failed');
      }

      setUploadStatus('success');
      setFile(null);
      
      const fileInput = document.getElementById('knowledge-file') as HTMLInputElement;
      if (fileInput) fileInput.value = '';
      
      // Refresh the document list
      fetchDocuments();
    } catch (error: any) {
      setUploadStatus('error');
      setErrorMessage(error.message || "An unexpected error occurred.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="flex flex-col gap-6 max-w-4xl mx-auto p-4 md:p-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-gray-900">Settings & Knowledge Base</h1>
        <p className="text-gray-500 mt-2">Manage your AI Receptionist's configurations and what it knows about your business.</p>
      </div>

      <div className="bg-white border rounded-lg shadow-sm overflow-hidden">
        <div className="p-6 border-b">
          <h3 className="text-lg font-semibold text-gray-900">Upload Knowledge Document</h3>
          <p className="text-sm text-gray-500 mt-1">
            Upload a PDF or TXT file containing information about your business. The AI will learn from this document and use it to answer customer queries.
          </p>
        </div>
        
        <div className="p-6">
          <div className="grid gap-4">
            <div className="grid w-full max-w-sm items-center gap-1.5">
              <label htmlFor="knowledge-file" className="text-sm font-medium text-gray-700">Document</label>
              <input 
                id="knowledge-file" 
                type="file" 
                accept=".pdf,.txt" 
                onChange={handleFileChange}
                disabled={isUploading}
                className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
              />
            </div>
            
            {uploadStatus === 'success' && (
              <div className="flex items-center gap-2 text-sm text-green-700 bg-green-50 border border-green-200 p-3 rounded-md">
                <span>✓ Document successfully uploaded and processed by the AI!</span>
              </div>
            )}
            
            {uploadStatus === 'error' && (
              <div className="flex items-center gap-2 text-sm text-red-700 bg-red-50 border border-red-200 p-3 rounded-md">
                <span>⚠ Error: {errorMessage}</span>
              </div>
            )}
          </div>
        </div>
        
        <div className="bg-gray-50 px-6 py-4 border-t">
          <button 
            onClick={handleUpload} 
            disabled={!file || isUploading}
            className="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 bg-blue-600 text-white hover:bg-blue-700 h-10 px-4 py-2 disabled:opacity-50 disabled:pointer-events-none w-full sm:w-auto"
          >
            {isUploading ? 'Processing...' : 'Upload and Learn'}
          </button>
        </div>
      </div>
      
      <div className="bg-white border rounded-lg shadow-sm overflow-hidden">
        <div className="p-6 border-b">
          <h3 className="text-lg font-semibold text-gray-900">Uploaded Documents</h3>
          <p className="text-sm text-gray-500 mt-1">Here is the list of documents the AI currently has memorized.</p>
        </div>
        <div className="p-6">
          {documents.length === 0 ? (
            <p className="text-sm text-gray-400 italic">No documents uploaded yet.</p>
          ) : (
            <ul className="divide-y divide-gray-100">
              {documents.map((doc, idx) => (
                <li key={idx} className="py-3 flex justify-between items-center group">
                  <div className="flex flex-col">
                    <span className="text-sm font-medium text-gray-900">{doc.title}</span>
                    <span className="text-xs text-gray-500">{new Date(doc.created_at).toLocaleDateString()}</span>
                  </div>
                  <button 
                    onClick={() => handleDelete(doc.id)}
                    className="text-red-500 hover:text-red-700 text-sm font-medium opacity-0 group-hover:opacity-100 transition-opacity focus:opacity-100"
                  >
                    Delete
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
      
      <div className="bg-white border rounded-lg shadow-sm overflow-hidden">
        <div className="p-6 border-b">
          <h3 className="text-lg font-semibold text-gray-900">AI Persona Settings</h3>
          <p className="text-sm text-gray-500 mt-1">Configure how your receptionist sounds and behaves.</p>
        </div>
        <div className="p-6">
          <p className="text-sm text-gray-400 italic mt-2">Coming soon...</p>
        </div>
      </div>
    </div>
  );
}
