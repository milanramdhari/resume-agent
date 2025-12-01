"use client";

import { useState } from "react";
import ReactDiffViewer, { DiffMethod } from "react-diff-viewer-continued";

export default function Home() {
  const [resumeLatex, setResumeLatex] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [tailoredLatex, setTailoredLatex] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showDiff, setShowDiff] = useState(false);

  const handleTailor = async () => {
    if (!resumeLatex || !jobDescription) {
      setError("Please provide both Resume LaTeX and Job Description.");
      return;
    }
    setLoading(true);
    setError("");
    setTailoredLatex("");

    try {
      const response = await fetch("http://localhost:8000/tailor", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ resumeLatex, jobDescription }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Something went wrong");
      }

      setTailoredLatex(data.tailoredLatex);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-8 bg-gray-50 text-gray-900 font-sans relative">
      <header className="mb-8 text-center">
        <h1 className="text-4xl font-bold text-blue-600 mb-2">Resume Tailor Agent</h1>
        <p className="text-gray-600">Tailor your LaTeX resume to any job description using AI.</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-7xl mx-auto">
        {/* Input Section */}
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <span className="bg-blue-100 text-blue-600 py-1 px-3 rounded-full text-sm">1</span>
              Resume LaTeX
            </h2>
            <textarea
              className="w-full h-64 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
              placeholder="\documentclass{article}..."
              value={resumeLatex}
              onChange={(e) => setResumeLatex(e.target.value)}
            />
          </div>

          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <span className="bg-blue-100 text-blue-600 py-1 px-3 rounded-full text-sm">2</span>
              Job Description
            </h2>
            <textarea
              className="w-full h-48 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
              placeholder="Paste the job description here..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
            />
          </div>

          <button
            onClick={handleTailor}
            disabled={loading}
            className={`w-full py-4 px-6 rounded-lg text-white font-semibold text-lg transition-all ${loading
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700 shadow-lg hover:shadow-xl"
              }`}
          >
            {loading ? "Tailoring Resume..." : "Tailor My Resume ✨"}
          </button>

          {error && (
            <div className="p-4 bg-red-50 text-red-700 rounded-lg border border-red-200">
              {error}
            </div>
          )}
        </div>

        {/* Output Section */}
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 h-full flex flex-col">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold flex items-center gap-2">
                <span className="bg-green-100 text-green-600 py-1 px-3 rounded-full text-sm">3</span>
                Tailored Result
              </h2>
              <div className="flex gap-2">
                {tailoredLatex && (
                  <>
                    <button
                      onClick={() => setShowDiff(true)}
                      className="text-sm bg-purple-100 text-purple-700 hover:bg-purple-200 py-1 px-3 rounded-md font-medium transition-colors"
                    >
                      Preview Changes
                    </button>
                    <button
                      onClick={() => navigator.clipboard.writeText(tailoredLatex)}
                      className="text-sm bg-gray-100 text-gray-700 hover:bg-gray-200 py-1 px-3 rounded-md font-medium transition-colors"
                    >
                      Copy Code
                    </button>
                  </>
                )}
              </div>
            </div>
            <textarea
              readOnly
              className="w-full flex-grow min-h-[600px] p-4 border border-gray-300 rounded-lg bg-gray-50 font-mono text-sm focus:outline-none"
              placeholder="Your tailored LaTeX code will appear here..."
              value={tailoredLatex}
            />
          </div>
        </div>
      </div>

      {/* Diff Modal */}
      {showDiff && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-2xl w-full max-w-7xl h-[90vh] flex flex-col overflow-hidden">
            <div className="p-4 border-b border-gray-200 flex justify-between items-center bg-gray-50">
              <h3 className="text-xl font-bold text-gray-800">Changes Preview</h3>
              <button
                onClick={() => setShowDiff(false)}
                className="text-gray-500 hover:text-gray-700 p-2 rounded-full hover:bg-gray-200 transition-colors"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="flex-grow overflow-auto p-4 bg-white">
              <ReactDiffViewer
                oldValue={resumeLatex}
                newValue={tailoredLatex}
                splitView={true}
                compareMethod={DiffMethod.WORDS}
                styles={{
                  variables: {
                    light: {
                      diffViewerBackground: '#fff',
                      diffViewerTitleBackground: '#f8f8f8',
                      gutterBackground: '#f8f8f8',
                      gutterBackgroundDark: '#f3f1f1',
                      addedBackground: '#e6ffec',
                      addedGutterBackground: '#cdffd8',
                      removedBackground: '#ffebe9',
                      removedGutterBackground: '#ffd7d5',
                      wordAddedBackground: '#acf2bd',
                      wordRemovedBackground: '#fdb8c0',
                    }
                  }
                }}
              />
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
