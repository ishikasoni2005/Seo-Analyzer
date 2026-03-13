import { useDeferredValue, useEffect, useState } from 'react';

import KeywordTable from '../components/KeywordTable';
import ReadabilityCard from '../components/ReadabilityCard';
import Suggestions from '../components/Suggestions';
import TextInput from '../components/TextInput';
import { analyzeText } from '../services/api';

const STORAGE_KEY = 'seo-analyzer-draft';
const SAMPLE_TEXT =
  'Search engine optimization helps brands attract qualified traffic, but many teams publish content without measuring keyword balance or readability. A strong SEO workflow reviews topic coverage, keeps sentences clear, and introduces related search terms naturally so pages can rank without sounding forced.';

function Analyzer() {
  const [text, setText] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const deferredText = useDeferredValue(text);

  useEffect(() => {
    const savedDraft = window.localStorage.getItem(STORAGE_KEY);
    if (savedDraft) {
      setText(savedDraft);
    } else {
      setText(SAMPLE_TEXT);
    }
  }, []);

  useEffect(() => {
    if (deferredText) {
      window.localStorage.setItem(STORAGE_KEY, deferredText);
    }
  }, [deferredText]);

  async function handleAnalyze() {
    if (!text.trim()) {
      setError('Add some copy first so the analyzer has content to inspect.');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const result = await analyzeText(text);
      setAnalysis(result);
    } catch (requestError) {
      const message =
        requestError.response?.data?.detail ||
        'The analyzer could not reach the backend. Check your API URL and Django server.';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }

  function handleLoadSample() {
    setText(SAMPLE_TEXT);
    setAnalysis(null);
    setError('');
  }

  return (
    <main className="page-shell">
      <section className="hero-panel">
        <div>
          <p className="eyebrow">SEO Analyzer Platform</p>
          <h1>Turn raw copy into search-ready content with a cleaner workflow.</h1>
          <p className="hero-copy">
            Review keyword density, readability, related keyword opportunities, and a lightly
            optimized draft from one screen.
          </p>
        </div>
        <div className="hero-stats">
          <div>
            <strong>TextRazor</strong>
            <span>External keyword enrichment</span>
          </div>
          <div>
            <strong>spaCy</strong>
            <span>NLP-assisted keyword placement</span>
          </div>
          <div>
            <strong>DRF API</strong>
            <span>Scalable backend delivery</span>
          </div>
        </div>
      </section>

      <section className="workspace-grid">
        <TextInput
          text={text}
          onTextChange={setText}
          onAnalyze={handleAnalyze}
          onLoadSample={handleLoadSample}
          isLoading={isLoading}
        />
        <ReadabilityCard score={analysis?.readability_score ?? 0} />
      </section>

      {error ? <p className="status-message error-message">{error}</p> : null}

      <section className="results-grid">
        <KeywordTable keywords={analysis?.keywords ?? []} />
        <Suggestions
          suggestedKeywords={analysis?.suggested_keywords ?? []}
          seoSuggestions={analysis?.seo_suggestions ?? []}
          optimizedText={
            analysis?.optimized_text ||
            'Run an analysis to preview a lightly optimized version of the draft.'
          }
        />
      </section>
    </main>
  );
}

export default Analyzer;
