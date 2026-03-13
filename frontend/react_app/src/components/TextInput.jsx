function TextInput({
  text,
  onTextChange,
  onAnalyze,
  onLoadSample,
  isLoading,
}) {
  const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
  const characterCount = text.length;

  return (
    <section className="panel input-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Content Studio</p>
          <h2>Paste the copy you want to optimize</h2>
        </div>
        <button type="button" className="ghost-button" onClick={onLoadSample}>
          Load sample
        </button>
      </div>

      <label className="input-label" htmlFor="seo-text-input">
        Article or landing-page draft
      </label>
      <textarea
        id="seo-text-input"
        className="text-area"
        placeholder="Write or paste your content here. Aim for enough context so keyword extraction and readability scoring are meaningful."
        value={text}
        onChange={(event) => onTextChange(event.target.value)}
      />

      <div className="input-meta">
        <span>{wordCount} words</span>
        <span>{characterCount} characters</span>
      </div>

      <button
        type="button"
        className="primary-button"
        onClick={onAnalyze}
        disabled={isLoading || !text.trim()}
      >
        {isLoading ? 'Analyzing draft...' : 'Analyze SEO'}
      </button>
    </section>
  );
}

export default TextInput;
