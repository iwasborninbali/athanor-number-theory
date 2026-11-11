import concurrent.futures,hashlib,json,pathlib,urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[1]
targets={
 'haiwalsh2010.pdf':'https://www.impan.pl/shop/publication/transaction/download/product/83626',
 'wnt2017.pdf':'https://westcoastnumbertheory.org/wp-content/uploads/2018/12/wcnt-problems-2017.pdf',
 'li2024.pdf':'https://nntdm.net/papers/nntdm-30/NNTDM-30-4-825-831.pdf',
 'walsh_survey.pdf':'https://www.cs.umd.edu/~gasarch/open/garyw.pdf',
 'walsh2026.pdf':'https://arxiv.org/pdf/2603.05809',
 'walsh_bibliography.html':'https://sites.google.com/view/gary-walsh/research-articles',
 'lin_walsh_yuan_abstract.pdf':'https://publi.math.unideb.hu/paper/2444/abstract/10_5486_PMD_2021_8928_abstract.pdf',
 'walsh_squares.pdf':'https://www.worldscientific.com/doi/pdf/10.1142/S1793042124500106',
 'lin_walsh_yuan_full.pdf':'https://publi.math.unideb.hu/paper/2444/download/10_5486_PMD_2021_8928.pdf',
}
def fetch(item):
 name,url=item
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (independent mathematical source audit)'})
  with urllib.request.urlopen(req,timeout=20) as r:
   data=r.read(4*1024**2); final=r.url;ctype=r.headers.get('content-type')
  if name.endswith('.pdf') and not data.startswith(b'%PDF'):name=name.removesuffix('.pdf')+'_response.html'
  (ROOT/'sources'/name).write_bytes(data)
  return dict(url=url,final_url=final,path='sources/'+name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),content_type=ctype)
 except Exception as e:return dict(url=url,error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(fetch,targets.items()))
(ROOT/'evidence/fetch_primary.json').write_text(json.dumps(rows,indent=2)+'\n')
for r in rows: print(r)
