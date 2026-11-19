import React, {useEffect, useState} from "react";
import {BrainCircuit, LayoutDashboard, FileUp, Target, BookOpen, LogOut, GraduationCap, ChevronRight, CheckCircle2, AlertCircle, FileDown} from "lucide-react";
import { generateReportPdf } from "./generatePdf";

const API = "http://127.0.0.1:5000/api";
export default function App(){
  const [token,setToken]=useState(localStorage.getItem("token")||"");
  const [student,setStudent]=useState(null);
  const [mode,setMode]=useState("login");
  const [form,setForm]=useState({name:"",email:"",password:""});
  const [roles,setRoles]=useState([]);
  const [roleId,setRoleId]=useState("");
  const [resume,setResume]=useState(null);
  const [marks,setMarks]=useState("");
  const [report,setReport]=useState(null);
  const [loading,setLoading]=useState(false);
  const [downloading,setDownloading]=useState(false);
  const [error,setError]=useState("");
  const [page,setPage]=useState("dashboard");

  useEffect(()=>{fetch(API+"/roles").then(r=>r.json()).then(setRoles).catch(()=>{});},[]);
  useEffect(()=>{if(token){fetch(API+"/me",{headers:{Authorization:"Bearer "+token}}).then(r=>r.json()).then(d=>{if(d.student_id)setStudent(d);else logout();}).catch(()=>setError("Cannot connect to backend. Start Flask first."));}},[token]);
  function logout(){localStorage.removeItem("token");setToken("");setStudent(null);setReport(null);}
  async function submitAuth(e){
    e.preventDefault();setError("");setLoading(true);
    try{
      const res=await fetch(API+(mode==="login"?"/login":"/register"),{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(form)});
      const data=await res.json();if(!res.ok)throw new Error(data.error||"Request failed");
      if(mode==="register"){setMode("login");setError("Account created. Please log in.");}
      else{localStorage.setItem("token",data.token);setToken(data.token);}
    }catch(e){setError(e.message);}finally{setLoading(false);}
  }
  async function analyze(e){
    e.preventDefault();setError("");if(!resume||!roleId){setError("Please choose a resume and target role.");return;}
    setLoading(true);const fd=new FormData();fd.append("resume",resume);fd.append("role_id",roleId);fd.append("marks",marks);
    try{const res=await fetch(API+"/analyze",{method:"POST",headers:{Authorization:"Bearer "+token},body:fd});const data=await res.json();if(!res.ok)throw new Error(data.error||"Analysis failed");setReport(data);setPage("results");}
    catch(e){setError(e.message);}finally{setLoading(false);}
  }
  async function downloadPdf(){
    if(!report)return;
    setDownloading(true);
    try{
      const res=await fetch(API+"/report/pdf",{
        method:"POST",
        headers:{
          "Content-Type":"application/json",
          Authorization:"Bearer "+token
        },
        body:JSON.stringify({report})
      });
      if(res.ok){
        const blob=await res.blob();
        const url=window.URL.createObjectURL(blob);
        const a=document.createElement("a");
        a.href=url;
        const roleSlug=(report.role||"Career").replace(/[^a-zA-Z0-9]/g,"_");
        a.download=`SkillGapReport_${roleSlug}.pdf`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      }else{
        generateReportPdf(report,student);
      }
    }catch(err){
      try{
        generateReportPdf(report,student);
      }catch(clientErr){
        setError("Could not generate PDF: "+(clientErr.message||err.message));
      }
    }finally{
      setDownloading(false);
    }
  }
  if(!token||!student) return <div className="auth-wrap"><div className="auth-card"><div className="brand large"><span className="brand-icon"><BrainCircuit/></span><div>SkillPath <b>AI</b><small>Career readiness, made personal</small></div></div><h1>{mode==="login"?"Welcome back":"Create your account"}</h1><p className="muted">Understand your skills. Discover your next step.</p><form onSubmit={submitAuth}>{mode==="register"&&<label>Full name<input required value={form.name} onChange={e=>setForm({...form,name:e.target.value})} placeholder="Your name"/></label>}<label>Email address<input type="email" required value={form.email} onChange={e=>setForm({...form,email:e.target.value})} placeholder="you@example.com"/></label><label>Password<input type="password" minLength="6" required value={form.password} onChange={e=>setForm({...form,password:e.target.value})} placeholder="At least 6 characters"/></label><button className="primary full" disabled={loading}>{loading?"Please wait...":mode==="login"?"Sign in":"Create account"}</button></form>{error&&<p className="notice">{error}</p>}<p className="switch">{mode==="login"?"New to SkillPath AI?":"Already registered?"} <button className="link" onClick={()=>{setMode(mode==="login"?"register":"login");setError("");}}>{mode==="login"?"Create an account":"Sign in"}</button></p></div></div>;

  const maxScore=Math.max(1,...(report?.report||[]).map(x=>x.score));
  return <div className="app"><aside className="sidebar"><div className="brand"><span className="brand-icon"><BrainCircuit/></span><div>SkillPath <b>AI</b><small>STUDENT PORTAL</small></div></div><div className="nav-label">WORKSPACE</div><button className={page==="dashboard"?"nav active":"nav"} onClick={()=>setPage("dashboard")}><LayoutDashboard/> Dashboard</button><button className={page==="analyze"?"nav active":"nav"} onClick={()=>setPage("analyze")}><FileUp/> Analyze resume</button>{report&&<button className={page==="results"?"nav active":"nav"} onClick={()=>setPage("results")}><Target/> Skill gap report</button>}<div className="side-bottom"><div className="student-mini"><div className="avatar">{student.name?.[0]?.toUpperCase()}</div><div><b>{student.name}</b><small>Student account</small></div></div><button className="nav" onClick={logout}><LogOut/> Sign out</button></div></aside>
  <main className="main"><header className="topbar"><div><span className="crumb">Workspace</span><ChevronRight size={14}/><b>{page==="dashboard"?"Dashboard":page==="analyze"?"Resume analysis":"Skill gap report"}</b></div><div className="top-right"><span className="status-dot"></span> Free learning workspace</div></header>
  <div className="content">
  {page==="dashboard"&&<><div className="welcome"><div><span className="eyebrow">YOUR CAREER JOURNEY</span><h1>Good to see you, {student.name.split(" ")[0]}.</h1><p>Turn your current skills into a clear plan for your target career.</p></div><button className="primary" onClick={()=>setPage("analyze")}><FileUp size={17}/> Start skill analysis</button></div><div className="hero-card"><div><span className="hero-tag">AI-POWERED CAREER READINESS</span><h2>Know where you stand.<br/>Plan where to go next.</h2><p>Upload your resume and compare your skills with the requirements of your dream job role.</p><button className="white-btn" onClick={()=>setPage("analyze")}>Analyze my skills <ChevronRight size={16}/></button></div><div className="hero-art"><div className="orbit orbit1"></div><div className="orbit orbit2"></div><div className="brain"><BrainCircuit size={72}/></div><div className="float-chip chip1">Skills <b>↗</b></div><div className="float-chip chip2">Career fit <b>AI</b></div></div></div><div className="section-head"><div><h2>How it works</h2><p className="muted">Three simple steps to your learning roadmap</p></div></div><div className="steps"><div className="step-card"><span className="step-icon blue"><FileUp/></span><span className="step-no">STEP 01</span><h3>Upload your resume</h3><p>Share your PDF or DOCX resume to extract your existing skills.</p></div><div className="step-card"><span className="step-icon purple"><Target/></span><span className="step-no">STEP 02</span><h3>Choose a career role</h3><p>Compare your profile with the skills required for your target job.</p></div><div className="step-card"><span className="step-icon green"><BookOpen/></span><span className="step-no">STEP 03</span><h3>Get your roadmap</h3><p>See your highest-priority gaps and relevant learning resources.</p></div></div><div className="info-note"><GraduationCap/><div><b>Built for student growth</b><p>Your report is a learning guide, not a hiring or placement score. Review your self-assessed levels for better results.</p></div></div></>}
  {page==="analyze"&&<><div className="page-title"><span className="eyebrow">AI SKILL ASSESSMENT</span><h1>Analyze your skills</h1><p>Upload your resume and choose a career role to generate your personalized report.</p></div><div className="form-card"><form onSubmit={analyze}><div className="form-section"><div className="form-heading"><span>01</span><div><h3>Upload your resume</h3><p>Supported formats: PDF and DOCX · Maximum 5 MB</p></div></div><label className="upload-box"><input type="file" accept=".pdf,.docx" onChange={e=>setResume(e.target.files[0])}/><span className="upload-icon"><FileUp/></span><b>{resume?resume.name:"Choose your resume file"}</b><small>{resume?"File selected successfully":"Click to browse your device"}</small></label></div><div className="form-section"><div className="form-heading"><span>02</span><div><h3>Select your target job role</h3><p>We will compare your skills against this role's requirements.</p></div></div><label>Target career role<select required value={roleId} onChange={e=>setRoleId(e.target.value)}><option value="">Select a job role</option>{roles.map(r=><option value={r.role_id} key={r.role_id}>{r.display_order ? `${r.display_order}. ${r.role_name}` : r.role_name}</option>)}</select></label></div><div className="form-section"><div className="form-heading"><span>03</span><div><h3>Academic marks (optional)</h3><p>Enter your overall percentage for your profile record.</p></div></div><label>Overall marks (%)<input type="number" min="0" max="100" value={marks} onChange={e=>setMarks(e.target.value)} placeholder="e.g. 78"/></label></div>{error&&<p className="notice"><AlertCircle size={16}/>{error}</p>}<button className="primary" disabled={loading}>{loading?"Analyzing resume...":"Generate skill gap report"} <ChevronRight size={17}/></button></form></div></>}
  {page==="results"&&report&&<><div className="page-header-row"><div className="page-title"><span className="eyebrow">YOUR ANALYSIS</span><h1>Skill gap report</h1><p>Target role: <b>{report.role}</b> · Review your current level and learning priorities.</p></div><div className="action-buttons"><button className="primary" onClick={downloadPdf} disabled={downloading}><FileDown size={16}/> {downloading?"Preparing PDF...":"Download PDF Report"}</button></div></div><div className="summary-grid"><div className="summary-card"><span>Skills detected in resume</span><strong>{report.extracted_skills.length}</strong><small>Matched skill terms</small></div><div className="summary-card"><span>Skills evaluated</span><strong>{report.report.length}</strong><small>Requirements for {report.role}</small></div><div className="summary-card"><span>Skills to improve</span><strong>{report.report.filter(x=>x.gap>0).length}</strong><small>Have a positive gap</small></div></div><div className="panel"><div className="panel-head"><div><h2>Current vs required skill levels</h2><p>Levels are measured on a 0–100 scale.</p></div><span className="legend"><i className="current"></i> Current <i className="required"></i> Required</span></div>{report.report.map(item=><div className="skill-row" key={item.skill}><div className="skill-label"><b>{item.skill}</b><span>Gap: {item.gap} · Priority score: {item.score}</span></div><div className="bars"><div className="bar-track"><div className="bar current" style={{width:item.current+"%"}}></div></div><div className="bar-track"><div className="bar required" style={{width:item.required+"%"}}></div></div></div></div>)}</div><div className="panel"><div className="panel-head"><div><h2>Priority learning areas</h2><p>Ranked by weighted gap score, highest first.</p></div></div>{report.report.slice(0,5).map((x,i)=><div className="priority-row" key={x.skill}><span className="rank">{i+1}</span><div><b>{x.skill}</b><small>{x.gap===0?"Requirement met":"Recommended focus area"}</small></div><strong>{x.score} pts</strong><div className="priority-track"><div style={{width:(x.score/maxScore*100)+"%"}}/></div></div>)}</div><div className="panel"><div className="panel-head"><div><h2>Recommended learning resources</h2><p>Free learning resources linked to your skill gaps.</p></div></div><div className="course-grid">{report.recommendations.map((c,i)=><div className="course" key={i}><span className="course-icon"><BookOpen/></span><div><b>{c.title}</b><small>{c.provider} · {c.level}</small><a href={c.url} target="_blank" rel="noreferrer">Explore course ↗</a></div></div>)}</div>{report.recommendations.length===0&&<p className="muted">No course recommendations available for this report.</p>}</div><div className="info-note"><CheckCircle2/><div><b>How to interpret this report</b><p>{report.note}</p></div></div><div className="report-actions"><button className="primary" onClick={downloadPdf} disabled={downloading}><FileDown size={16}/> {downloading?"Preparing PDF...":"Download PDF Report"}</button><button className="secondary" onClick={()=>setPage("analyze")}>Run another analysis</button></div></>}
  </div></main></div>
}
