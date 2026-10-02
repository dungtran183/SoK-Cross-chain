"""Reference audit: resolve every cited DOI through doi.org content negotiation
(Crossref / DataCite) and write verified BibTeX to ../refs_raw.bib; log failures."""
import os, re, sys, time, requests
KB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS = {
 # surveys / SoKs
 "zamyatin2021sok": "10.1007/978-3-662-64331-0_1", "haugum2022security": "10.1145/3530019.3531345",
 "lee2023sok": "10.1109/icbc56567.2023.10174993", "duan2023attacks": "10.1109/jas.2023.123642",
 "zhang2024security": "10.1145/3678890.3678894", "notland2024sok": "10.48550/arxiv.2403.00405",
 "augusto2024sok": "10.1109/sp54263.2024.00255", "belenkov2025sok": "10.48550/arxiv.2501.03423",
 "zhou2023sok": "10.1109/SP46215.2023.10179435", "belchior2021survey": "10.1145/3471140",
 # attacks / empirical
 "judmayer2021pay": "10.1007/978-3-662-63958-0_39", "xue2021hedging": "10.1145/3465084.3467904",
 "zhang2022jamming": "10.1109/iucc-cit-dsci-smartcns57392.2022.00034", "lin2024fake": "10.1109/iscas58744.2024.10558359",
 "wu2025safeguarding": "10.1145/3696410.3714604", "yan2025empirical": "10.1145/3708821.3733878",
 "mukherjee2025double": "10.1016/j.bcra.2025.100378", "azad2025hedge": "10.48550/arxiv.2507.06156",
 "liu2025phantom": "10.48550/arxiv.2502.13513", "hu2025jigsaw": "10.1145/3744970.3727306",
 "li2025walls": "10.48550/arxiv.2511.15245", "augusto2026liquidity": "10.48550/arxiv.2602.17805",
 "arote2026mind": "10.1109/icbc67748.2026.11575511", "zhang2026stalled": "10.1145/3777912.3839782",
 "cao2026price": "10.1145/3805650",
 # runtime / response
 "zhang2022xscope": "10.1145/3551349.3559520", "liu2024monte": "10.48550/arxiv.2410.01107",
 "augusto2025xchainwatcher": "10.1145/3721462.3770781", "eshghie2024highguard": "10.1145/3691620.3695356",
 "ganguly2022runtime": "10.1109/icdcs54860.2022.00012", "winkler2026brigade": "10.1007/978-3-032-32575-4_16",
 "wiputra2025bads": "10.1109/caisais68078.2025.11440752", "lin2025bridgeshield": "10.48550/arxiv.2508.20517",
 "liang2025cifgviewer": "10.1007/978-981-95-4142-3_44", "lin2024gmmcct": "10.1145/3659463.3660008",
 "tran2025veribridge": "10.1109/vcris68011.2025.11250562", "augusto2025looking": "10.1109/dsn-s65789.2025.00025",
 "hu2024reputation": "10.1109/tnsm.2024.3433414", "yi2024ccctm": "10.1016/j.ins.2024.120930",
 "tran2025acheron": "10.1016/j.iot.2025.101836", "tran2026crosstrust": "10.1109/JIOT.2026.3671650",
 "liang2025connex": "10.48550/arxiv.2511.01393", "lin2025track": "10.1109/tsc.2025.3618729",
 "augusto2025xchaindatagen": "10.48550/arxiv.2503.13637", "mateus2025pausing": "10.1109/brains67003.2025.11302954",
 "kwon2026killswitch": "10.1109/jiot.2026.3686857", "wu2026tracing": "10.48550/arxiv.2607.18869",
 # pre-deployment
 "liao2024smartaxe": "10.1145/3643738", "zhou2025bridgeguard": "10.1109/tdsc.2025.3576114",
 "wang2024xguard": "10.1145/3663529.3663809", "winkler2026bridgefuzz": "10.1145/3803525.3804980",
 "augusto2026intentfuzz": "10.48550/arxiv.2609.13004", "liu2026eventspec": "10.48550/arxiv.2609.07865",
 "tran2024chainsniper": "10.1145/3654522.3654577", "tran2026crossguard": "10.1007/s10586-026-06298-0",
 "tran2026evoexploit": "10.1016/j.asoc.2026.116561", "maric2025failsafe": "10.4230/oasics.fmbc.2025.8",
 # design time
 "gazi2019pos": "10.1109/sp.2019.00040", "bentov2019tesseract": "10.1145/3319535.3363221",
 "tefagh2020tamarin": "10.4230/oasics.fmbc.2020.5", "zarick2021layerzero": "10.48550/arxiv.2110.13871",
 "xiong2022trustboost": "10.1145/3576915.3623080", "xie2022zkbridge": "10.1145/3548606.3560652",
 "tsai2023ibc": "10.1109/icnp59255.2023.10355573", "si2024cross": "10.1016/j.comcom.2024.05.012",
 "ivycross2025": "10.1109/tmc.2025.3562875", "p2c2t2025": "10.1109/sp61157.2025.00051",
 "sampling2025": "10.4230/lipics.aft.2025.31", "pipeswap2025": "10.1109/sp61157.2025.00245",
 "mercury2026": "10.1109/tdsc.2025.3630656", "zkhtlc2026": "10.1016/j.comnet.2026.112780",
 "zamyatin2019xclaim": "10.1109/SP.2019.00085", "fourswap2025": "10.48550/arxiv.2508.04641",
 # methodology / own background
 "page2021prisma": "10.1136/bmj.n71", "tran2026fedvuln": "10.1016/j.future.2025.108264",
 "tran2026chronosrep": "10.1016/j.ins.2026.123323",
}
H = {"Accept": "application/x-bibtex; charset=utf-8", "User-Agent": "reference-audit/1.0"}
out, fails = [], []
for key, doi in REFS.items():
    bib = None
    for _ in range(3):
        try:
            r = requests.get(f"https://doi.org/{doi}", headers=H, timeout=40)
            if r.ok and r.text.strip().startswith("@"):
                bib = r.text.strip(); break
        except requests.RequestException:
            pass
        time.sleep(2)
    if bib is None:
        fails.append((key, doi)); print("FAIL", key, doi, flush=True); continue
    bib = re.sub(r"^@(\w+)\{[^,]*,", lambda m: f"@{m.group(1)}{{{key},", bib, count=1)
    out.append(bib)
    print("ok", key, flush=True)
    time.sleep(0.4)
open(os.path.join(os.path.dirname(KB), "refs_raw.bib"), "w", encoding="utf-8").write("\n\n".join(out) + "\n")
open(os.path.join(KB, "prisma/reference_audit.log"), "w").write("\n".join(f"FAIL {k} {d}" for k, d in fails) + f"\nresolved {len(out)}/{len(REFS)}\n")
print("resolved", len(out), "/", len(REFS))
