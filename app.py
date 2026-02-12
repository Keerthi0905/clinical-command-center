from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(_name_)

# Data Stores
patients = []
activity_feed = [] 
discharged_archive = [] 
visit_tracker = {}  
master_registry = {} 

def log_activity(msg, category="info", broadcast=False):
    now = datetime.now().strftime("%H:%M:%S")
    activity_feed.append({"ts": now, "msg": msg, "type": category, "broadcast": broadcast})

@app.route('/')
def home():
    dept_filter = request.args.get('dept', 'All')
    # Filter center pathway based on department selection
    filtered_patients = patients if dept_filter == 'All' else [p for p in patients if p['current_dept'] == dept_filter]

    stats = {
        "critical_count": len([p for p in patients if p['priority'] == 'Emergency' and p['current_dept'] != 'Discharge']),
        "total_active": len([p for p in patients if p['current_dept'] != 'Discharge']),
        "total_discharged": len(discharged_archive)
    }
    
    return render_template('index.html', 
                           patients=filtered_patients, 
                           stats=stats, 
                           feed=activity_feed[::-1][:10], 
                           archive=discharged_archive[::-1],
                           dept=dept_filter)

@app.route('/register', methods=['POST'])
def register():
    now_ts = datetime.now().strftime("%H:%M")
    p_name = request.form.get('name')
    p_age = request.form.get('age')
    
    unique_key = f"{p_name}_{p_age}"
    if unique_key not in master_registry:
        master_registry[unique_key] = len(master_registry) + 1
    
    internal_id = master_registry[unique_key]
    visit_tracker[internal_id] = visit_tracker.get(internal_id, 0) + 1
    
    new_patient = {
        "id": len(patients) + 1,
        "patient_uid": internal_id,
        "name": p_name,
        "visit_count": visit_tracker[internal_id],
        "age": p_age,
        "priority": request.form.get('priority'),
        "current_dept": "Reception",
        "orders": {"rx": [], "lab": []},
        "audit_trail": [{"ts": now_ts, "user": "Admin", "action": "Admitted"}]
    }
    patients.append(new_patient)
    log_activity(f"NEW ENTRY: {p_name} registered.", "info", broadcast=True)
    return redirect(url_for('home'))

@app.route('/update_clinical/<int:p_id>', methods=['POST'])
def update_clinical(p_id):
    now_ts = datetime.now().strftime("%H:%M")
    for p in patients:
        if p['id'] == p_id:
            detail = request.form.get('detail')
            p['orders']['lab'].append({"test": detail, "status": "Ordered"})
            p['audit_trail'].append({"ts": now_ts, "user": "Clinical", "action": f"Ordered {detail}"})
    return redirect(url_for('home'))

@app.route('/transition/<int:p_id>', methods=['POST'])
def transition(p_id):
    target_dept = request.form.get('target_dept')
    for p in patients:
        if p['id'] == p_id:
            p['current_dept'] = target_dept
            p['audit_trail'].append({"ts": datetime.now().strftime("%H:%M"), "user": "System", "action": f"Moved to {target_dept}"})
            
            if target_dept == "Discharge":
                p['audit_trail'].append({"ts": datetime.now().strftime("%H:%M"), "user": "Admin", "action": "Discharge Summary Finalized"})
                if p not in discharged_archive:
                    discharged_archive.append(p)
    return redirect(url_for('home', dept=target_dept))

if _name_ == '_main_':
    app.run(debug=True)
