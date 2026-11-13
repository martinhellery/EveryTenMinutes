import urllib.request, json, time, sys, io
def raw(u):
    for i in range(6):
        try:
            return urllib.request.urlopen(urllib.request.Request('https://mempool.space/api'+u,headers={'User-Agent':'x'}),timeout=60).read()
        except Exception as e:
            time.sleep(2+i*2)
    raise RuntimeError(u)
def varint(b,i):
    n=b[i]
    if n<0xfd: return n,i+1
    if n==0xfd: return int.from_bytes(b[i+1:i+3],'little'),i+3
    if n==0xfe: return int.from_bytes(b[i+1:i+5],'little'),i+5
    return int.from_bytes(b[i+1:i+9],'little'),i+9
def parse(b):
    i=80
    n,i=varint(b,i)
    res=[]
    for t in range(n):
        i+=4
        seg=False
        if b[i]==0 and b[i+1]==1:
            seg=True; i+=2
        nin,i=varint(b,i)
        for _ in range(nin):
            i+=36
            l,i=varint(b,i); i+=l+4
        nout,i=varint(b,i)
        outs=[]
        for _ in range(nout):
            i+=8
            l,i=varint(b,i)
            outs.append(b[i:i+l]); i+=l
        ord_env=False
        if seg:
            for _ in range(nin):
                ni,i=varint(b,i)
                for _ in range(ni):
                    l,i=varint(b,i)
                    item=b[i:i+l]; i+=l
                    if b'\x00\x63\x03ord' in item: ord_env=True
        i+=4
        res.append((outs,ord_env))
    assert i==len(b),(i,len(b))
    return res
if __name__=='__main__':
    start,end,stride=930340,969923,int(sys.argv[1])
    out=[]
    for h in range(start+stride//2,end,stride):
        hh=raw(f'/block-height/{h}').decode()
        b=raw(f'/block/{hh}/raw')
        txs=parse(b)
        n=len(txs)-1  # exclude coinbase
        runes=sum(1 for outs,_ in txs[1:] if any(o[:2]==b'\x6a\x5d' for o in outs))
        opr=sum(1 for outs,_ in txs[1:] if any(o[:1]==b'\x6a' for o in outs))
        ordi=sum(1 for _,e in txs[1:] if e)
        out.append(dict(h=h,hash=hh,n=n,runes=runes,opreturn=opr,ord=ordi))
        print(out[-1],flush=True)
        time.sleep(0.3)
    json.dump(out,open('runes_sample.json','w'))
    N=sum(o['n'] for o in out)
    print('blocks',len(out),'tx',N,'runes',sum(o['runes'] for o in out)/N,'opreturn',sum(o['opreturn'] for o in out)/N,'ord',sum(o['ord'] for o in out)/N)
