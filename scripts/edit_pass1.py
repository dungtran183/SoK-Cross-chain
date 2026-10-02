import re
p = r"C:\Users\dungt\Downloads\PhD\ACIIDS2027-SoK\main.tex"
s = open(p, encoding="utf-8").read()
drop = ['ganguly2022runtime', 'eshghie2024highguard', 'liang2025cifgviewer', 'tefagh2020tamarin',
        'bentov2019tesseract', 'sampling2025', 'si2024cross', 'hu2024reputation', 'arote2026mind']


def fix(m):
    keys = [k.strip() for k in m.group(1).split(',') if k.strip() not in drop]
    return '\\cite{' + ','.join(keys) + '}' if keys else 'CITEGONE'


s = re.sub(r'\\cite\{([^}]*)\}', fix, s)
s = s.replace('; bridge delays enable liquidity poisoning of multi-hop arbitrage~CITEGONE;', ';')
assert 'CITEGONE' not in s, [l for l in s.split('\n') if 'CITEGONE' in l]

a = s.index('\\subsubsection{Related reviews.}')
b = s.index('\\begin{table}[t]', a)
s = s[:a] + ("\\subsubsection{Related reviews.} Table~\\ref{tab:related} positions this review against earlier "
             "surveys of interoperability~\\cite{zamyatin2021sok,belchior2021survey,haugum2022security,duan2023attacks}, "
             "incident reviews~\\cite{lee2023sok,belenkov2025sok} and security SoKs~\\cite{zhang2024security,notland2024sok,augusto2024sok}. "
             "It differs in three ways: it is organized by lifecycle stage rather than by mechanism or incident, it formalizes "
             "attack classes as property violations, and it covers 116 studies published in 2024 to 2026 that postdate most "
             "earlier reviews.\n\n") + s[b:]

old_hdr = ("Review & Method & Period & Incidents & Attack--property & Lifecycle & Learning-based \\\\\n"
           " & & & mapped & formalization & mapping & detectors \\\\")
new_hdr = ("Review & Method & Period & Incid. & Property & Life- & Learned \\\\\n"
           " & & & mapped & formal. & cycle & detectors \\\\")
assert old_hdr in s
s = s.replace(old_hdr, new_hdr)
open(p, 'w', encoding='utf-8').write(s)
print("ok")
