# -*- coding: utf-8 -*-
"""符号登记审计 —— 扫描手稿数学段中的符号，对照《符号登记表》报告未登记与字形不符。

用法：
    python scripts/symbol_audit.py <手稿.md> [更多.md ...] [--registry 符号登记表.md]
    python scripts/symbol_audit.py --scaffold <手稿.md> ... [--out 新登记表.md] [--force]

审计：对照登记表报未登记/字形不符/\text（报告不代改）。
骨架：--scaffold 从手稿提取全部须登记符号，生成登记表骨架（现形/频次自动填，
语义与规范字形留待人工/AI 裁定）——登记表正本的语义列不可全自动再生。

缺省登记表 = 首个手稿同目录的 符号登记表.md。
报告不代改：未登记符号由人工/AI 登记进表并在表内记录（登记表 §2 应用与增补记录）。

判定口径（与 references/math-typesetting.md 一致）：
  - 裸单字母（无下标/重音/粗体）= R1 标量，放行不查（登记表"其余标量"行为兜底行）；
  - 带下标、撇号、重音（\\dot/\\hat/\\bar/\\tilde）、矢量/张量粗体、多字母正体 = 须登记；
  - 算子/函数（sin、exp、\\nabla、\\mathrm{d} 等）与单位（mm、Pa 等）跳过；
  - 身份 = 字母串 + 归一化下标（去 \\mathrm 外壳与花括号）——d_n 与 d_\\mathrm{n} 同身份，
    但字形以登记表为准 → 报"字形不符"；
  - \\text{} 使用本身即违规（统一 \\mathrm），单列报告。

退出码：0 = 全登记且无发现；1 = 有未登记/字形不符/\\text；2 = 输入或脚本错误。
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

# %% ---------------- 常量：跳过集 ----------------
OPERATORS = {  # 函数/算子/LaTeX 命令，不算符号
    'sin', 'cos', 'tan', 'cot', 'sec', 'csc', 'exp', 'ln', 'log', 'sinh', 'cosh',
    'tanh', 'arctan', 'arcsin', 'arccos', 'max', 'min', 'lim', 'tr', 'det',
    'Gamma', 'nabla', 'partial', 'square', 'mathrm', 'boldsymbol', 'mathbf',
    'text', 'tag', 'frac', 'dfrac', 'tfrac', 'left', 'right', 'cdot', 'times',
    'overset', 'underset', 'dot', 'hat', 'bar', 'tilde', 'overline',
    'approx', 'sim', 'simeq', 'propto', 'quad', 'qquad', 'le', 'leq', 'leqslant',
    'ge', 'geq', 'geqslant', 'gg', 'll', 'in', 'infty', 'sum', 'prod', 'sqrt',
    'dots', 'cdots', 'ldots', 'circ', 'pm', 'mp', 'div', 'perp', 'parallel',
    'big', 'Big', 'bigl', 'bigr', 'Bigl', 'Bigr', 'bigm', 'begin', 'end',
    'mathcal', 'mathbb', 'operatorname', 'stackrel', 'displaystyle', 'limits',
    'int', 'iint', 'prime', 'angle', 'forall', 'exists',
}
ROMAN_SKIP = {'d', 'D', 'dx', 'dy', 'dz', 'dt', 'tr'}  # \mathrm{} 里的微分/算子
UNITS = {  # \mathrm{} 里的常见单位
    'mm', 'cm', 'm', 'um', 'nm', 'km', 's', 'ms', 'min', 'h', 'g', 'kg', 'mg',
    'N', 'mN', 'Pa', 'kPa', 'MPa', 'mPa', 'K', 'mol', 'L', 'mL', 'W', 'J', 'Kg',
}
DIMLESS_KNOWN = {'Re', 'Wi', 'We', 'Fr', 'Ca', 'De', 'Oh', 'El', 'Pr', 'Sc', 'Pe'}

# %% ---------------- 数学段抽取 ----------------
FENCE = re.compile(r'```.*?```', re.S)
CODESPAN = re.compile(r'`[^`\n]+`')
DISPLAY = re.compile(r'\$\$(.+?)\$\$', re.S)
INLINE = re.compile(r'\$([^$\n]+?)\$')
TEXTCMD = re.compile(r'\\text\s*\{([^{}]*)\}')
BEGEND = re.compile(r'\\(?:begin|end)\s*\{[^{}]*\}')

def math_segments(text):
    """返回 [(行号, 数学串)]；先剥代码块/行内代码，再取 $$…$$ 与 $…$。"""
    text = FENCE.sub('', text)
    text = CODESPAN.sub('', text)
    out = []
    for m in DISPLAY.finditer(text):
        line = text.count('\n', 0, m.start()) + 1
        out.append((line, m.group(1)))
        text = text[:m.start()] + ' ' * (m.end() - m.start()) + text[m.end():]
    for m in INLINE.finditer(text):
        line = text.count('\n', 0, m.start()) + 1
        out.append((line, m.group(1)))
    return out

# %% ---------------- 符号 token 识别 ----------------
TOK = re.compile(r'''
    \\boldsymbol\s*\{\s*\\mathrm\s*\{\s*(?P<gt>[A-Za-z]+)\s*\}\s*\}
  | \\boldsymbol\s*\{\s*(?P<vec>[A-Za-z]+)\s*\}
  | \\mathbf\s*\{\s*(?P<ten>[A-Za-z]+)\s*\}
  | \\mathrm\s*\{\s*(?P<rom>[A-Za-z]+)\s*\}
  | \\(?P<accname>dot|hat|bar|tilde|overline)(?![A-Za-z])\s*(?P<acc>(?:\\[A-Za-z]+|[A-Za-z]))
  | \\(?P<gr>[A-Za-z]+)
  | (?P<lat>[A-Za-z]+)
''', re.X)
SUB = re.compile(r'_\s*(?:\\mathrm\s*\{\s*([A-Za-z,]+)\s*\}|\{([A-Za-z,]+)\}|([A-Za-z]))')

def strip_sub(sub_raw):
    """下标归一化：去 \\mathrm 外壳、花括号、空白。"""
    if not sub_raw:
        return ''
    s = re.sub(r'\\(?:mathrm|boldsymbol|mathbf)\s*', '', sub_raw)
    return re.sub(r'[{}\s]', '', s)

def scan_tokens(mathstr):
    """返回 [(raw, kind, letters, sub, prime)]。"""
    mathstr = BEGEND.sub(' ', TEXTCMD.sub(' ', mathstr))  # \text 与 \begin/\end 参数不参与取符号
    toks = []
    for m in TOK.finditer(mathstr):
        d = m.groupdict()
        if d['gt'] is not None:
            kind, letters = 'gtensor', d['gt']
        elif d['vec'] is not None:
            kind, letters = 'vector', d['vec']
        elif d['ten'] is not None:
            kind, letters = 'tensor', d['ten']
        elif d['rom'] is not None:
            kind, letters = 'roman', d['rom']
        elif d['acc'] is not None:
            kind, letters = 'accent', d['accname'] + ':' + d['acc'].lstrip('\\')
        elif d['gr'] is not None:
            kind, letters = 'greek', d['gr']
        else:
            kind, letters = 'latin', d['lat']
        # 跳过：算子/函数、单位、微分正体
        if letters in OPERATORS or letters in ROMAN_SKIP or letters in UNITS:
            continue
        if kind == 'roman' and letters not in DIMLESS_KNOWN:
            continue  # 未知 \mathrm{词} 多为单位/缩写，不作未登记报（保守）
        # 吸附后随下标与撇号
        end = m.end(); sub = ''; prime = ''
        while True:
            sm = SUB.match(mathstr, end)
            if sm:
                sub += strip_sub(sm.group(1) or sm.group(2) or sm.group(3) or '')
                end = sm.end(); continue
            pm = re.match(r"\s*'", mathstr[end:])
            if pm:
                prime += "'"; end += pm.end(); continue
            break
        raw = mathstr[m.start():end].strip()
        toks.append((raw, kind, letters, sub, prime))
    return toks

def identity(tok):
    """身份：(字母, 下标, 撇号)；roman 与裸拉丁多字母视为同身份（无量纲正体纠错面）。"""
    _, kind, letters, sub, prime = tok
    return (letters, sub, prime)

def needs_registry(tok):
    """是否属'须登记'类：
    - 重音/粗体（矢量、张量）形式 → 须登记；
    - 带下标或撇号 → 须登记；
    - \\mathrm{词}（走到这里的已过滤单位/微分）→ 须登记；
    - 裸拉丁多字母：首字母大写 = 无量纲数候选（Re、Bd、Qt…）须查；全小写 = 并置乘积（如 ak）放行；
    - 裸单字母 / 裸希腊字母 → R1 标量放行（登记表'其余标量'行为兜底行）。
    """
    raw, kind, letters, sub, prime = tok
    if kind in ('accent', 'vector', 'tensor', 'gtensor'):
        return True
    if sub or prime:
        return True
    if kind == 'roman':
        return True
    if kind == 'latin' and len(letters) > 1:
        return letters[0].isupper()
    return False

# %% ---------------- 登记表解析 ----------------
BACKTICK = re.compile(r'`([^`\n]+)`')

def load_registry(path):
    """登记表内全部反引号片段按同一取词法解析 → {身份: 登记标准形}。"""
    reg = {}
    if not path or not Path(path).exists():
        return reg
    content = Path(path).read_text(encoding='utf-8')
    content = content.split('\n## 2', 1)[0]  # 只解析 §1 符号对照总表——应用记录里的历史写法不作登记形
    for snip in BACKTICK.findall(content):
        for tok in scan_tokens(snip):
            if needs_registry(tok):
                reg.setdefault(identity(tok), tok[0])
    return reg

# %% ---------------- 骨架生成（--scaffold） ----------------
def collect(ms_files):
    """跨手稿汇总须登记符号：{身份: {'forms': Counter(现形), 'first': (文件, 行)}}"""
    agg = {}
    for ms in ms_files:
        text = Path(ms).read_text(encoding='utf-8')
        for line, mstr in math_segments(text):
            for tok in scan_tokens(mstr):
                if not needs_registry(tok):
                    continue
                ent = agg.setdefault(identity(tok), {'forms': Counter(), 'first': (ms.name, line)})
                ent['forms'][tok[0]] += 1
    return agg

def scaffold(ms_files, out=None, force=False):
    """生成登记表骨架：现形/频次自动，语义与规范字形留待人工/AI。"""
    agg = collect(ms_files)
    lines = [
        '# 符号登记表（骨架 —— 脚本生成，语义待人工/AI 填写）',
        '',
        '> 由 symbol_audit.py --scaffold 从手稿生成。**"符号/类别/规范写法"三列须人工/AI 裁定**：'
        '符号列填语义描述，规范写法按 references/math-typesetting.md 校正字形'
        '（词缩写下标补 \\mathrm、无量纲数转正体等）；裁定完成前本表不具审计效力。',
        '',
        '## 1. 符号对照总表',
        '',
        '| 符号（语义待填） | 类别 | 规范写法（初判=手稿现形，待校正） | 现状 |',
        '|---|---|---|---|',
    ]
    rows = sorted(agg.items(), key=lambda kv: -sum(kv[1]['forms'].values()))
    for idt, ent in rows:
        form, n = ent['forms'].most_common(1)[0]
        variants = '、'.join(f'{k}×{v}' for k, v in ent['forms'].most_common(3))
        src = f"，首见 {ent['first'][0]} L{ent['first'][1]}"
        lines.append(f'| 待填 | 待填 | `{form}`（{n} 次{src}；变体 {variants}） | 待裁 |')
    lines += ['', '## 2. 应用与增补记录', '', '> （登记与批量统一在此留痕）', '']
    body = '\n'.join(lines)
    if out:
        p = Path(out)
        if p.exists() and not force:
            print(f'[错误] 目标已存在（防覆盖，加 --force 覆盖）：{p}'); sys.exit(2)
        p.write_text(body, encoding='utf-8')
        print(f'骨架已写出：{p}（{len(rows)} 项待裁定）')
    else:
        print(body)
    sys.exit(0)

# %% ---------------- 主流程 ----------------
def audit(ms_path, registry):
    text = Path(ms_path).read_text(encoding='utf-8')
    segs = math_segments(text)
    n_text = len(TEXTCMD.findall(text))
    found, unreg, mismatch = [], Counter(), {}
    for line, mstr in segs:
        for tok in scan_tokens(mstr):
            raw, kind = tok[0], tok[1]
            if not needs_registry(tok):
                continue
            idt = identity(tok)
            found.append((line, raw, idt))
            canon = registry.get(idt)
            if canon is None:
                unreg[(raw, idt)] += 1
            elif canon != raw:
                mismatch.setdefault((raw, canon), []).append(line)
    return segs, found, unreg, mismatch, n_text

def main():
    ap = argparse.ArgumentParser(description='手稿符号登记审计（报告不代改）')
    ap.add_argument('manuscripts', nargs='+', help='手稿 .md 路径（可多个）')
    ap.add_argument('--registry', help='符号登记表路径；缺省 = 首个手稿同目录 符号登记表.md')
    ap.add_argument('--scaffold', action='store_true', help='从手稿生成登记表骨架（不审计）')
    ap.add_argument('--out', help='骨架写出路径；缺省打印到屏幕')
    ap.add_argument('--force', action='store_true', help='允许覆盖已存在的 --out 文件')
    args = ap.parse_args()

    ms_files = [Path(p) for p in args.manuscripts]
    for p in ms_files:
        if not p.exists():
            print(f'[错误] 手稿不存在：{p}'); sys.exit(2)
    if args.scaffold:
        scaffold(ms_files, out=args.out, force=args.force)
    reg_path = Path(args.registry) if args.registry else ms_files[0].parent / '符号登记表.md'
    registry = load_registry(reg_path)
    print(f'登记表：{reg_path}（登记身份 {len(registry)} 项）')

    rc = 0
    for ms in ms_files:
        segs, found, unreg, mismatch, n_text = audit(ms, registry)
        print(f'\n== {ms.name}')
        print(f'数学段 {len(segs)} 处；须登记符号 {len(found)} 例（去重 {len({f[2] for f in found})} 身份）')
        if unreg:
            print(f'[未登记] {len(unreg)} 项 —— 请人工/AI 登记进符号登记表并记录：')
            for (raw, idt), n in sorted(unreg.items(), key=lambda x: -x[1]):
                first = min(l for l, r, i in found if i == idt)
                print(f'  - {raw}（身份 {"·".join(filter(None, idt))}，{n} 次，首见 L{first}）')
            rc = 1
        else:
            print('[未登记] 0')
        if mismatch:
            print(f'[字形不符] {len(mismatch)} 项 —— 以登记表为准批量统一：')
            for (raw, canon), lines in sorted(mismatch.items()):
                print(f'  - {raw}（L{lines[0]} 等 {len(lines)} 处）↔ 登记 {canon}')
            rc = 1
        if n_text:
            print(f'[\\text 使用] {n_text} 处 —— 统一改 \\mathrm')
            rc = 1
    sys.exit(rc)

if __name__ == '__main__':
    main()
