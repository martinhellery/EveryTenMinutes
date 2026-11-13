import urllib.request, json, time, statistics
def get(u):
    for i in range(5):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request('https://mempool.space/api'+u,headers={'User-Agent':'x'}),timeout=30))
        except Exception as e:
            time.sleep(2+i*2)
    raise
rows=[]
for h in range(930354, 969923, 150):
    for b in get(f'/v1/blocks/{h}'):
        rows.append((b['height'],b['timestamp'],b['tx_count']))
    time.sleep(0.15)
json.dump(rows,open('tx_sample.json','w'))
tx=[r[2] for r in rows]
print(len(rows), statistics.mean(tx), statistics.median(tx))
