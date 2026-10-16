#!/usr/bin/env python3
"""Source verification primitive — shared by authoring and the validator.

Fetches a URL via curl with a browser User-Agent (bypasses the bot-blocks that
403 WebFetch on thedailystar.net / tbsnews.net), converts HTML **or PDF** to
plain text, and either prints that text or checks whether a candidate verbatim
quote appears. PDF support uses poppler `pdftotext`.

Usage:
  python source_tool.py text  <url>                 # print cleaned article text
  python source_tool.py check <url> "<quote>"       # verify quote appears verbatim
  python source_tool.py checkfile <templates.jsonl> # batch-verify source+source_quote for every template
"""
import sys, os, subprocess, re, html, json, tempfile
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

def _norm_ws(h):
    h = h.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    h = re.sub(r"\s+", " ", h)
    return h.strip()

def clean(h):
    h = re.sub(r"(?is)<(script|style|noscript|svg|head)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"(?is)<!--.*?-->", " ", h)
    h = re.sub(r"(?s)<[^>]+>", " ", h)
    h = html.unescape(h)
    return _norm_ws(h)

def norm(s):
    s = html.unescape(s)
    return _norm_ws(s)

def fetch(url):
    """Return (http_code, cleaned_text). Handles HTML and PDF. Empty text on non-200."""
    fd, tmp = tempfile.mkstemp(suffix=".dat")
    os.close(fd)
    try:
        code = subprocess.run(
            ["curl", "-sSL", "-A", UA, "--max-time", "45", "-o", tmp, "-w", "%{http_code}", url],
            capture_output=True, text=True, timeout=70).stdout.strip()
    except Exception as e:
        _rm(tmp); return (f"ERR:{e}", "")
    if code != "200":
        _rm(tmp); return (code, "")
    try:
        with open(tmp, "rb") as f:
            head = f.read(5)
        is_pdf = head.startswith(b"%PDF") or url.lower().split("?")[0].endswith(".pdf")
        if is_pdf:
            try:
                txt = subprocess.run(["pdftotext", "-q", "-nopgbrk", tmp, "-"],
                                     capture_output=True, text=True, encoding="utf-8",
                                     errors="replace", timeout=90).stdout
            except Exception as e:
                return (f"PDFERR:{e}", "")
            return (code, _norm_ws(txt))
        with open(tmp, "rb") as f:
            body = f.read().decode("utf-8", "replace")
        return (code, clean(body))
    finally:
        _rm(tmp)

def _rm(p):
    try: os.unlink(p)
    except Exception: pass

def check(url, quote):
    code, text = fetch(url)
    if code != "200":
        return (code, False, None)
    present = norm(quote).lower() in text.lower()
    return (code, present, text)

def main():
    mode = sys.argv[1]
    if mode == "text":
        code, text = fetch(sys.argv[2])
        print(f"[HTTP {code}]  ({len(text)} chars)\n")
        print(text)
    elif mode == "check":
        code, present, _ = check(sys.argv[2], sys.argv[3])
        print(f"HTTP {code} | quote present verbatim: {present}")
        sys.exit(0 if present else 1)
    elif mode == "checkfile":
        T = [json.loads(l) for l in open(sys.argv[2], encoding="utf-8") if l.strip()]
        cache = {}
        allok = True
        for t in T:
            url, q = t["source"], t.get("source_quote", "")
            if url not in cache:
                cache[url] = fetch(url)
            code, text = cache[url]
            live = code == "200"
            present = live and norm(q).lower() in text.lower()
            status = "OK" if (live and present) else ("DEAD/BLOCKED" if not live else "QUOTE-MISSING")
            if not (live and present):
                allok = False
            print(f"{t['template_id']:<9} HTTP {str(code):<8} quote={'Y' if present else 'N'}  {status}")
        print("\nALL SOURCES + QUOTES VERIFIED" if allok else "\nSOME FAILED — see above")
        sys.exit(0 if allok else 1)

if __name__ == "__main__":
    main()
