export default function RiskBadge({level='LOW'}){return <span className={`badge ${level.toLowerCase().replace(' ','-')}`}><i/>{level}</span>}
