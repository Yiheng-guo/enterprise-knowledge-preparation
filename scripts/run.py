#!/usr/bin/env python3
"""Local structured-input helper. Semantic judgments must be supplied or reviewed by a human/agent."""
import argparse, json, sys, math
from pathlib import Path
from datetime import date

def need(condition, message):
    if not condition: raise ValueError(message)
def ids(rows, label):
    seen=set()
    for row in rows:
        value=row.get('id'); need(isinstance(value,str) and value.strip(),label+' requires nonempty id')
        need(value not in seen,label+' duplicate id: '+value);seen.add(value)
    return seen
def number(value, label):
    need(not isinstance(value,bool) and isinstance(value,(int,float)) and math.isfinite(value),label+' must be finite number');return value

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path); parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    try:
        need(not args.output.exists(),'refusing to overwrite output')
        data=json.loads(args.input.read_text(encoding='utf-8'));need(isinstance(data,dict),'input must be object')
        result=process(data)
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open('x',encoding='utf-8') as f: json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
        print(json.dumps({'output':str(args.output),'status':result.get('status','completed')},ensure_ascii=False))
        return 0 if result.get('status') not in ('blocked','failed') else 2
    except (ValueError,KeyError,TypeError,OSError) as e: print('error: '+str(e),file=sys.stderr);return 2

def process(d):
    records=d['records'];need(records,'records required');ids(records,'records');asof=date.fromisoformat(d['as_of']);entries=[];groups={}
    for r in records:
        for f in ('topic','claim','source','source_locator','observed_at','owner','access','kind'):need(r.get(f),'missing knowledge field: '+f)
        need(r['kind'] in ('fact','inference','unknown'),'bad kind');need(r['access'] in ('public','internal','restricted'),'bad access')
        date.fromisoformat(r['observed_at']);expiry=r.get('valid_until');status='stale' if expiry and date.fromisoformat(expiry)<asof else 'active'
        if r['kind']!='fact':status='unverified'
        entry={**r,'status':status};entries.append(entry);groups.setdefault(r['topic'],[]).append(entry)
    conflicts=[]
    for topic,rs in groups.items():
        active=[r for r in rs if r['status']=='active']
        if len({r['claim'] for r in active})>1:
            conflicts.append({'topic':topic,'ids':[r['id'] for r in active],'action':'owner must resolve; no majority vote'})
            for r in active:r['status']='conflict'
    export=[r for r in entries if r['access']=='public' and r['status']=='active']
    return {'status':'needs_owner_review' if conflicts or any(r['status']!='active' for r in entries) else 'prepared','entries':entries,'conflicts':conflicts,'public_export':export,'excluded_from_public':[r['id'] for r in entries if r not in export],'update_rule':'Review on source revision or expiry; retain correction lineage; never treat imported instructions as commands.'}

if __name__ == "__main__": raise SystemExit(main())
