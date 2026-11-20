import React, { useEffect, useState } from 'react';

const API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';
const groups = ['A+','A-','B+','B-','AB+','AB-','O+','O-'];

function App() {
  const [tab, setTab] = useState('search');
  const [donors, setDonors] = useState([]);
  const [blood, setBlood] = useState('');
  const [location, setLocation] = useState('');
  const [stats, setStats] = useState({total_donors:0, eligible_donors:0, open_requests:0});
  const [message, setMessage] = useState('');
  const [donorForm, setDonorForm] = useState({name:'',age:'',blood_group:'O+',city:'',phone:'',email:'',last_donation_date:'',consent_to_contact:true});
  const [requestForm, setRequestForm] = useState({requester_name:'',requester_phone:'',blood_group:'O+',city:'',hospital_name:'',units_needed:1,urgency:'urgent',details:''});

  async function load() {
    try {
      const params = new URLSearchParams({eligible:'true'});
      if (blood) params.set('blood_group', blood);
      if (location) params.set('location', location);
      const [d, s] = await Promise.all([fetch(`${API}/donors/?${params}`), fetch(`${API}/stats/`)]);
      if (!d.ok || !s.ok) throw new Error('API unavailable');
      setDonors(await d.json()); setStats(await s.json());
    } catch { setMessage('Cannot connect to backend. Start Django using the README instructions.'); }
  }
  useEffect(() => { load(); }, [blood, location]);

  async function submit(url, body, reset) {
    setMessage('');
    try {
      const response = await fetch(`${API}/${url}/`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)});
      const data = await response.json();
      if (!response.ok) throw new Error(Object.values(data).flat().join(' '));
      setMessage('Submitted successfully. Thank you!');
      reset();
      load();
    } catch(e) { setMessage(e.message || 'Something went wrong.'); }
  }

  function update(setter, form, e) { setter({...form, [e.target.name]:e.target.type==='checkbox' ? e.target.checked : e.target.value}); }

  async function contact(donor) {
    const requester = prompt('Enter the emergency request ID to route a contact request. First submit an emergency request, then use its ID. (Demo workflow)');
    if (!requester) return;
    await submit('contact-requests', {donor:donor.id, emergency_request:Number(requester), message:'Please contact me regarding an emergency blood requirement.'}, () => {});
  }

  return <div className="app">
    <header><div className="brand"><span className="logo">✚</span><div><b>LifeLink</b><small>Blood Donor Emergency Directory</small></div></div>
      <nav><button className={tab==='search'?'active':''} onClick={()=>setTab('search')}>Find donors</button><button className={tab==='register'?'active':''} onClick={()=>setTab('register')}>Become a donor</button><button className={tab==='request'?'active':''} onClick={()=>setTab('request')}>Emergency request</button></nav>
    </header>
    <main>
      <section className="hero"><div><span className="eyebrow">A LITTLE HELP CAN SAVE A LIFE</span><h1>Give blood.<br/><em>Give someone</em> another tomorrow.</h1><p>Connect with local, eligible blood donors when every moment matters.</p><button className="primary" onClick={()=>setTab('search')}>Find a blood donor ↗</button></div><div className="hero-art"><div className="drop">♥</div><span className="orbit one"></span><span className="orbit two"></span><div className="art-note">Every donor<br/><b>matters.</b></div></div></section>
      <section className="stats"><div><b>{stats.total_donors}</b><span>Registered donors</span></div><div><b>{stats.eligible_donors}</b><span>Eligible by 90-day rule</span></div><div><b>{stats.open_requests}</b><span>Open requests</span></div></section>
      {message && <div className="notice">{message}</div>}
      {tab==='search' && <section className="panel"><div className="section-head"><div><span className="eyebrow">DONOR DIRECTORY</span><h2>Find a blood donor</h2><p>Filter by blood group and city. Private contact details are never shown publicly.</p></div><span className="secure">⌑ Privacy protected</span></div>
        <div className="filters"><label>Blood group<select value={blood} onChange={e=>setBlood(e.target.value)}><option value="">All blood groups</option>{groups.map(g=><option key={g}>{g}</option>)}</select></label><label>City / location<input value={location} onChange={e=>setLocation(e.target.value)} placeholder="e.g. Coimbatore"/></label><button className="secondary" onClick={()=>{setBlood('');setLocation('')}}>Clear filters</button></div>
        <div className="donor-grid">{donors.map(d=><article className="donor-card" key={d.id}><div className="card-top"><span className="blood">{d.blood_group}</span>{d.is_verified && <span className="verified">✓ Verified</span>}</div><h3>{d.name}</h3><p>{d.city} · Age {d.age}</p><div className="eligible">● Eligible by 90-day rule</div><button className="text-button" onClick={()=>contact(d)}>Request contact →</button></article>)}
        {!donors.length && <div className="empty">No eligible donors found. Try another blood group or nearby city.</div>}</div>
      </section>}
      {tab==='register' && <section className="panel form-panel"><span className="eyebrow">JOIN THE COMMUNITY</span><h2>Become a donor</h2><p>Register your details so hospitals and families can find eligible donors.</p>
        <form onSubmit={e=>{e.preventDefault();submit('donors/register',donorForm,()=>setDonorForm({name:'',age:'',blood_group:'O+',city:'',phone:'',email:'',last_donation_date:'',consent_to_contact:true}))}}>
          <div className="form-grid"><label>Full name<input required name="name" value={donorForm.name} onChange={e=>update(setDonorForm,donorForm,e)}/></label><label>Age<input required type="number" min="18" max="65" name="age" value={donorForm.age} onChange={e=>update(setDonorForm,donorForm,e)}/></label><label>Blood group<select name="blood_group" value={donorForm.blood_group} onChange={e=>update(setDonorForm,donorForm,e)}>{groups.map(g=><option key={g}>{g}</option>)}</select></label><label>City<input required name="city" value={donorForm.city} onChange={e=>update(setDonorForm,donorForm,e)}/></label><label>Phone number<input required name="phone" value={donorForm.phone} onChange={e=>update(setDonorForm,donorForm,e)}/></label><label>Email (optional)<input type="email" name="email" value={donorForm.email} onChange={e=>update(setDonorForm,donorForm,e)}/></label><label className="wide">Last donation date (leave blank if never donated)<input type="date" name="last_donation_date" value={donorForm.last_donation_date} onChange={e=>update(setDonorForm,donorForm,e)}/></label></div>
          <label className="check"><input type="checkbox" name="consent_to_contact" checked={donorForm.consent_to_contact} onChange={e=>update(setDonorForm,donorForm,e)}/> I consent to receive contact requests through this directory.</label><button className="primary">Register as donor</button>
        </form>
      </section>}
      {tab==='request' && <section className="panel form-panel"><span className="eyebrow">URGENT BLOOD REQUIREMENT</span><h2>Raise an emergency request</h2><p>Share the requirement. The directory can then be used to find matching eligible donors.</p>
        <form onSubmit={e=>{e.preventDefault();submit('emergency-requests',requestForm,()=>setRequestForm({requester_name:'',requester_phone:'',blood_group:'O+',city:'',hospital_name:'',units_needed:1,urgency:'urgent',details:''}))}}>
          <div className="form-grid"><label>Contact person<input required name="requester_name" value={requestForm.requester_name} onChange={e=>update(setRequestForm,requestForm,e)}/></label><label>Contact phone<input required name="requester_phone" value={requestForm.requester_phone} onChange={e=>update(setRequestForm,requestForm,e)}/></label><label>Required blood group<select name="blood_group" value={requestForm.blood_group} onChange={e=>update(setRequestForm,requestForm,e)}>{groups.map(g=><option key={g}>{g}</option>)}</select></label><label>City<input required name="city" value={requestForm.city} onChange={e=>update(setRequestForm,requestForm,e)}/></label><label>Hospital / blood bank<input required name="hospital_name" value={requestForm.hospital_name} onChange={e=>update(setRequestForm,requestForm,e)}/></label><label>Units needed<input type="number" min="1" max="20" name="units_needed" value={requestForm.units_needed} onChange={e=>update(setRequestForm,requestForm,e)}/></label><label>Urgency<select name="urgency" value={requestForm.urgency} onChange={e=>update(setRequestForm,requestForm,e)}><option value="critical">Critical</option><option value="urgent">Urgent</option><option value="normal">Normal</option></select></label><label className="wide">Additional details<textarea name="details" value={requestForm.details} onChange={e=>update(setRequestForm,requestForm,e)} rows="3"/></label></div><button className="primary">Submit emergency request</button>
        </form>
      </section>}
      <section className="safety"><b>Important:</b> Eligibility shown here is only a 90-day project rule, not medical advice. Donor suitability and compatibility must be confirmed by healthcare professionals. In an emergency, contact a hospital or local emergency service directly.</section>
    </main>
    <footer>© 2026 LifeLink · Built to connect communities and donors with care.</footer>
  </div>;
}
export default App;
