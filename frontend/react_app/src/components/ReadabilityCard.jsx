function getReadabilityLabel(score) {
  if (score >= 80) return 'Excellent clarity';
  if (score >= 65) return 'Easy to read';
  if (score >= 50) return 'Moderate difficulty';
  return 'Needs simplification';
}

function ReadabilityCard({ score }) {
  const gaugeWidth = `${Math.max(8, Math.min(score, 100))}%`;

  return (
    <section className="panel readability-panel">
      <p className="eyebrow">Readability</p>
      <h2>How accessible the copy feels</h2>
      <div className="score-row">
        <strong>{score}</strong>
        <span>{getReadabilityLabel(score)}</span>
      </div>
      <div className="gauge-track" aria-hidden="true">
        <div className="gauge-fill" style={{ width: gaugeWidth }} />
      </div>
      <p className="supporting-text">
        Higher scores usually mean a broader audience can scan and understand the page quickly.
      </p>
    </section>
  );
}

export default ReadabilityCard;
