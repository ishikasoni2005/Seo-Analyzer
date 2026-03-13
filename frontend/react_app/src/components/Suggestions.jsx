function Suggestions({ suggestedKeywords, seoSuggestions, optimizedText }) {
  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Optimization Ideas</p>
          <h2>Related terms and suggested refinements</h2>
        </div>
      </div>

      <div className="chip-group">
        {suggestedKeywords.length ? (
          suggestedKeywords.map((keyword) => (
            <span key={keyword} className="chip">
              {keyword}
            </span>
          ))
        ) : (
          <span className="empty-inline">No additional keyword suggestions yet.</span>
        )}
      </div>

      <div className="suggestions-list">
        <h3>SEO suggestions</h3>
        {seoSuggestions.length ? (
          <ul>
            {seoSuggestions.map((suggestion) => (
              <li key={suggestion}>{suggestion}</li>
            ))}
          </ul>
        ) : (
          <p className="empty-state">Your draft is already in a strong place.</p>
        )}
      </div>

      <div className="optimized-copy">
        <h3>Optimized text preview</h3>
        <p>{optimizedText}</p>
      </div>
    </section>
  );
}

export default Suggestions;
