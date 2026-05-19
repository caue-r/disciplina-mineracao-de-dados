"""
pip install pypdf
 
python parse_mare_cabedelo.py --pdf mareCabedelo.pdf --out mareCabedelo.csv
"""
 
import re
import csv
import argparse
from pathlib import Path
 
DIA_MAP = {
    "SEG": "Segunda-feira",
    "TER": "Terça-feira",
    "QUA": "Quarta-feira",
    "QUI": "Quinta-feira",
    "SEX": "Sexta-feira",
    "SÁB": "Sábado",
    "SAB": "Sábado",
    "DOM": "Domingo",
}
 
MES_MAP = {
    "Janeiro":   1,
    "Fevereiro": 2,
    "Março":     3,
    "Abril":     4,
    "Maio":      5,
    "Junho":     6,
    "Julho":     7,
    "Agosto":    8,
    "Setembro":  9,
    "Outubro":  10,
    "Novembro": 11,
    "Dezembro": 12,
}
 
RE_MES     = re.compile(r"^(" + "|".join(MES_MAP.keys()) + r")$")
RE_DIA_NUM = re.compile(r"^(\d{1,2})$")
RE_DIA_SEM = re.compile(r"^([A-ZÁÉÍÓÚÂÊÎÔÛÃÕÇ]{3})$", re.UNICODE)
RE_PAR     = re.compile(r"^(\d{4})\s+(-?\d+\.\d+)$")
 
 
def extrair_texto_pdf(caminho: str) -> str:
    from pypdf import PdfReader
    reader = PdfReader(caminho)
    return "\n".join(p.extract_text() or "" for p in reader.pages)
 
 
def classificar_mare(alturas: list, idx: int) -> str:
    h = alturas[idx]
    prev_ok = (idx == 0) or (h >= alturas[idx - 1])
    next_ok = (idx == len(alturas) - 1) or (h >= alturas[idx + 1])
    return "Preamar" if (prev_ok and next_ok) else "Baixa-mar"
 
 
def parsear_texto(texto: str, ano: int = 2025) -> list:
    registros = []
    mes_atual  = None
    dia_num    = None
    dia_sem    = None
    pares      = []
 
    def flush():
        if mes_atual is None or dia_num is None or not pares:
            return
        data_str = f"{ano:04d}-{mes_atual:02d}-{dia_num:02d}"
        alturas  = [alt for _, alt in pares]
        for idx, (hora_raw, alt) in enumerate(pares):
            hora_fmt = f"{hora_raw[:2]}:{hora_raw[2:]}"
            registros.append({
                "data":       data_str,
                "dia_semana": DIA_MAP.get(dia_sem, dia_sem),
                "hora":       hora_fmt,
                "altura_m":   alt,
                "tipo_mare":  classificar_mare(alturas, idx),
            })
 
    for linha in texto.splitlines():
        linha = linha.strip()
        if not linha:
            continue
 
        m = RE_MES.match(linha)
        if m:
            flush()
            pares, dia_num, dia_sem = [], None, None
            for k, v in MES_MAP.items():
                if k.lower() == linha.lower():
                    mes_atual = v
                    break
            continue
 
        m = RE_DIA_NUM.match(linha)
        if m:
            flush()
            pares, dia_sem = [], None
            dia_num = int(m.group(1))
            continue
 
        m = RE_DIA_SEM.match(linha)
        if m:
            abrev = m.group(1).upper()
            if abrev in DIA_MAP:
                dia_sem = abrev
            continue
 
        m = RE_PAR.match(linha)
        if m and dia_num is not None:
            pares.append((m.group(1), float(m.group(2))))
            continue
 
    flush()
    return registros
 
 
def escrever_csv(registros: list, caminho: str) -> None:
    campos = ["data", "dia_semana", "hora", "altura_m", "tipo_mare"]
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(registros)
 
 
def main():
    p = argparse.ArgumentParser(
        description="Converte tábua de marés do Porto de Cabedelo (PDF) → CSV."
    )
    p.add_argument("--pdf", default="23_-_porto_de_cabedelo_-_pb_-_77-79.pdf")
    p.add_argument("--out", default="mare_cabedelo_2025.csv")
    p.add_argument("--ano", type=int, default=2025)
    args = p.parse_args()
 
    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        raise SystemExit(f"Arquivo não encontrado: {pdf_path}")
 
    registros = parsear_texto(extrair_texto_pdf(str(pdf_path)), args.ano)
 
    if not registros:
        raise SystemExit("Nenhum registro encontrado.")
 
    escrever_csv(registros, args.out)
 
if __name__ == "__main__":
    main()
 