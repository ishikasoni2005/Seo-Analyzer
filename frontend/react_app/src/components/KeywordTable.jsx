function KeywordTable({ keywords }) {
  return (
    <section className="panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Keyword Breakdown</p>
          <h2>Top phrases detected in your draft</h2>
        </div>
      </div>

      {keywords.length ? (
        <div className="table-wrapper">
          <table className="keyword-table">
            <thead>
              <tr>
                <th>Keyword</th>
                <th>Frequency</th>
                <th>Density</th>
              </tr>
            </thead>
            <tbody>
              {keywords.map((keyword) => (
                <tr key={keyword.word}>
                  <td>{keyword.word}</td>
                  <td>{keyword.frequency}</td>
                  <td>{keyword.density}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p className="empty-state">
          No clear keywords were extracted yet. Add more topical detail and try again.
        </p>
      )}
    </section>
  );
}

export default KeywordTable;
