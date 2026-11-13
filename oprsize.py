import json,sys,time
sys.path.insert(0,'.')
from runes import raw,parse
d=json.load(open('runes_sample.json'))
out=[]
mx=0;big=0;tot=0
for x in d:
    try:
        b=raw(f"/block/{x['hash']}/raw")
        txs=parse(b)
    except Exception as e:
        print('err',x['h'],e,flush=True); continue
    sizes=[]
    for outs,_ in txs[1:]:
        for o in outs:
            if o[:1]==b'\x6a': sizes.append(len(o)-1)  # bytes after OP_RETURN opcode (incl push opcodes)
    mxb=max(sizes) if sizes else 0
    out.append(dict(h=x['h'],n_opr=len(sizes),max=mxb,over83=sum(1 for s in sizes if s>82)))
    print(out[-1],flush=True)
    time.sleep(0.2)
json.dump(out,open('oprsize.json','w'))
