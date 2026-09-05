import {Icon} from './Icons';
export default function StatCard({label,value,note,icon='chart',tone=''}){return <div className={`stat card ${tone}`}><div className="stat-icon"><Icon name={icon}/></div><p>{label}</p><h2>{value}</h2><small>{note}</small></div>}
