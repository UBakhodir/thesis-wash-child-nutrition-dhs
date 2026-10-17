--[[
thesis.lua -- pandoc Lua filter for the v12 thesis Markdown sources.

Conversion mechanics only. The filter never changes words, numbers,
citation keys or variable names. What it does:

 1. Headings. "# 5. Results", "## 5.6 Title", "# Appendix A — Title",
    "## A.1 Title" -> LaTeX \section / \subsection with the typed number
    removed (LaTeX numbers it) plus \label{sec:<number>} and
    \ThesisCheckNumber{<counter>}{<number>}, so a mismatch between the
    source number and LaTeX's number stops the build. "# Abstract" becomes
    an unnumbered section listed in the contents. Any other heading shape
    is an error, not a guess.
 2. Table captions. A paragraph that is entirely bold and reads
    "Table N.M — Title" becomes \ThesisTableCaption{N.M}{Title}
    (caption + \label{tab:N.M} + number check). It must be followed by a
    table, optionally after exactly one intervening paragraph (the bold
    sub-labels above Tables 5.5–5.7), which stays where it is. The caption
    therefore shows "Table 5.5" once, never twice.
 3. Tables. Column widths from content (see convert_table); a body row
    whose only non-empty cell is the first one (e.g. "| **Region FE** |")
    becomes a full-width group row.
 4. Unicode superscript characters (⁴ ⁵ ⁶ ⁸ ⁻ ...), several of which are
    missing from Times New Roman, become \textsuperscript{...} with the
    ordinary digits/minus sign. Same characters, rendered with a font that
    has them.
 5. Inline code spans become \ThesisCode{...} with permitted line breaks
    after / _ . - so long file paths wrap instead of overflowing.
 6. A fenced div  ::: {.tablenote} ... :::  is typeset in the 9pt/13.5pt
    table-note style (not used by the v12 sources; available if approved).
 7. Appendix tables only (caption number "A.1", "B.2", ...): the table gets
    a separate first head and, on every continuation page, a line
    "Table A.1 (continued)" above the repeated column heads (added in the
    Appendix A session). Chapter tables (numbers "5.1", ...) are written
    exactly as before.

Citations are not touched here: pandoc's --biblatex writer turns [@key]
into \autocite{key} and [-@key] into \autocite*{key}.
]]

local stringify = pandoc.utils.stringify

local function latex_inlines(inlines)
  return pandoc.write(pandoc.Pandoc({ pandoc.Plain(inlines) }), 'latex',
    { cite_method = 'biblatex', wrap_text = 'none' }):gsub('%s+$', '')
end

local function fail(msg)
  error('[thesis.lua] ' .. msg, 0)
end

-- Drop the first `n` words (Str elements) and the spaces after them.
local function drop_words(inlines, n)
  local out, dropped, i = pandoc.List(), 0, 1
  while i <= #inlines and dropped < n do
    local el = inlines[i]
    if el.t == 'Str' then dropped = dropped + 1
    elseif el.t ~= 'Space' and el.t ~= 'SoftBreak' then
      fail('unexpected element in heading/caption number prefix: ' .. el.t)
    end
    i = i + 1
  end
  while i <= #inlines and (inlines[i].t == 'Space' or inlines[i].t == 'SoftBreak') do i = i + 1 end
  for j = i, #inlines do out:insert(inlines[j]) end
  return out
end

local LEVEL_CMD = { 'section', 'subsection', 'subsubsection', 'paragraph' }
local DASHES = { ['—'] = true, ['–'] = true, ['--'] = true, ['---'] = true }

local function convert_header(h)
  local text = stringify(h.content)
  local level = h.level
  if level > 4 then fail('heading level ' .. level .. ' is not allowed: ' .. text) end
  local cmd = LEVEL_CMD[level]

  if level == 1 and text == 'Abstract' then
    return pandoc.RawBlock('latex',
      '\\section*{Abstract}\\label{sec:abstract}\\addcontentsline{toc}{section}{Abstract}')
  end

  local number, body
  if level == 1 then
    local letter, dash = text:match('^Appendix (%u) (%S+) ')
    if letter and DASHES[dash] then
      number, body = letter, drop_words(h.content, 3)
    else
      local n = text:match('^(%d+)%. ')
      if n then number, body = n, drop_words(h.content, 1) end
    end
  else
    local pat = '^(%w+' .. string.rep('%.%d+', level - 1) .. ') '
    local n = text:match(pat)
    if n and (n:match('^%d+%.') or n:match('^%u%.')) then
      number, body = n, drop_words(h.content, 1)
    end
  end
  if not number then
    fail('heading has no recognisable level-' .. level .. ' number: "' .. text .. '"')
  end

  local title = latex_inlines(body)
  return pandoc.RawBlock('latex', string.format(
    '\\%s{%s}\\label{sec:%s}\\ThesisCheckNumber{%s}{%s}', cmd, title, number, cmd, number))
end

-- "**Table 5.5 — Title**" -> number, title inlines (or nil)
local function table_caption(block)
  if block.t ~= 'Para' or #block.content ~= 1 or block.content[1].t ~= 'Strong' then
    return nil
  end
  local inl = block.content[1].content
  local num, dash = stringify(inl):match('^Table (%w+%.%d+) (%S+) ')
  if not num or not DASHES[dash] then return nil end
  return num, drop_words(inl, 3)
end

local SUP = { ['⁰']='0', ['¹']='1', ['²']='2', ['³']='3', ['⁴']='4', ['⁵']='5',
  ['⁶']='6', ['⁷']='7', ['⁸']='8', ['⁹']='9', ['⁺']='+', ['⁻']='−' }

local function split_superscripts(s)
  local out, buf, sup = pandoc.List(), '', ''
  for _, c in utf8.codes(s) do
    local ch = utf8.char(c)
    if SUP[ch] then
      if buf ~= '' then out:insert(pandoc.Str(buf)); buf = '' end
      sup = sup .. SUP[ch]
    else
      if sup ~= '' then out:insert(pandoc.Superscript({ pandoc.Str(sup) })); sup = '' end
      buf = buf .. ch
    end
  end
  if buf ~= '' then out:insert(pandoc.Str(buf)) end
  if sup ~= '' then out:insert(pandoc.Superscript({ pandoc.Str(sup) })) end
  return out
end

local function has_superscript(s)
  for _, c in utf8.codes(s) do if SUP[utf8.char(c)] then return true end end
  return false
end

local CODE_ESC = {
  ['\\'] = '\\textbackslash{}', ['{'] = '\\{', ['}'] = '\\}', ['$'] = '\\$',
  ['&'] = '\\&', ['#'] = '\\#', ['%'] = '\\%', ['~'] = '\\textasciitilde{}',
  ['^'] = '\\textasciicircum{}',
  -- permitted (zero-width) line breaks after path/identifier separators
  ['_'] = '\\_\\allowbreak{}', ['/'] = '/\\allowbreak{}',
  ['.'] = '.\\allowbreak{}', ['-'] = '-\\allowbreak{}',
}

local function latex_escape_code(s)
  local out = {}
  for _, c in utf8.codes(s) do
    local ch = utf8.char(c)
    out[#out + 1] = CODE_ESC[ch] or ch
  end
  return table.concat(out)
end

local inline_filter = {
  Str = function(el)
    if has_superscript(el.text) then return split_superscripts(el.text) end
  end,
  Code = function(el)
    return pandoc.RawInline('latex', '\\ThesisCode{' .. latex_escape_code(el.text) .. '}')
  end,
}

local function ulen(str)
  return utf8.len(str) or #str
end

-- Text used only to estimate a cell's width: code spans (already raw LaTeX
-- here) are unescaped, split at their permitted break points and widened by
-- 35% (monospace is wider than average Times text); math loses its markup.
local function measure_text(blocks)
  local b = pandoc.Blocks(blocks):walk({
    RawInline = function(r)
      local t = r.text:match('^\\ThesisCode{(.*)}$')
      if not t then return nil end
      t = t:gsub('\\allowbreak{}', ' '):gsub('\\textbackslash{}', '\\'):gsub('\\(.)', '%1')
      t = t:gsub('%S+', function(w) return w .. string.rep('m', math.ceil(ulen(w) * 0.35)) end)
      return pandoc.Str(t)
    end,
    Math = function(m)
      return pandoc.Str((m.text:gsub('\\%a+', ''):gsub('[{}_^%s]', '')))
    end,
  })
  return stringify(b)
end

local function is_group_row(row, ncol)
  if ncol < 2 or #row.cells ~= ncol then return false end
  if stringify(row.cells[1].contents) == '' then return false end
  for i = 2, ncol do
    if stringify(row.cells[i].contents) ~= '' then return false end
  end
  return true
end

-- Approximate capacity of one table line in characters: 14.5 cm text width
-- at 10 pt Times New Roman (about 4.6 bp per character on average), less
-- inter-column padding.
local LINE_CHARS = 88

--[[ Column widths ("water-filling"). L = longest cell text, W = longest
  single word (+2 slack). Columns whose full text fits within an equal share
  of the remaining capacity get their full width, so short columns (labels,
  N, coefficients) never wrap; the remaining capacity is then shared by the
  long columns in proportion to L, never below W. ]]
local function convert_table(tbl)
  local ncol = #tbl.colspecs
  local L, W = {}, {}
  for i = 1, ncol do L[i] = 3; W[i] = 3 end
  local function measure(row)
    for i, cell in ipairs(row.cells) do
      if i <= ncol then
        local txt = measure_text(cell.contents)
        L[i] = math.max(L[i], ulen(txt))
        -- +2 characters of slack: wide letters and cell padding
        for word in txt:gmatch('%S+') do W[i] = math.max(W[i], ulen(word) + 2) end
      end
    end
  end
  for _, row in ipairs(tbl.head.rows) do measure(row) end
  for _, body in ipairs(tbl.bodies) do
    for _, row in ipairs(body.body) do
      if is_group_row(row, ncol) then
        local cell = row.cells[1]
        cell.col_span = ncol
        row.cells = pandoc.List({ cell })
      else
        measure(row)
      end
    end
  end
  local cap = LINE_CHARS - 2 * ncol
  local w, open, remaining = {}, {}, cap
  for i = 1, ncol do L[i] = math.max(L[i], W[i]); open[i] = true end
  local changed = true
  while changed do
    changed = false
    local n = 0
    for i = 1, ncol do if open[i] then n = n + 1 end end
    if n == 0 then break end
    local share = remaining / n
    for i = 1, ncol do
      if open[i] and L[i] <= share then
        w[i] = L[i]; open[i] = false; remaining = remaining - L[i]; changed = true
      end
    end
  end
  local sumOpen = 0
  for i = 1, ncol do if open[i] then sumOpen = sumOpen + L[i] end end
  for i = 1, ncol do
    if open[i] then w[i] = math.max(W[i], remaining * L[i] / sumOpen) end
  end
  local total = 0
  for i = 1, ncol do total = total + w[i] end
  for i = 1, ncol do
    tbl.colspecs[i] = { pandoc.AlignLeft, w[i] / total }
  end
  return tbl
end

-- Appendix tables (item 7): write the table to LaTeX here and give it a
-- first head plus a continuation head "Table X.N (continued)".
local function continued_table(tbl, num)
  local tex = pandoc.write(pandoc.Pandoc({ tbl }), 'latex',
    { cite_method = 'biblatex', wrap_text = 'preserve' })
  local top = '\\toprule\\noalign{}\n'
  local h0, h1 = tex:find(top, 1, true)
  local e0, e1 = tex:find('\\endhead', 1, true)
  if not h0 or not e0 or e0 < h1 then
    fail('appendix table ' .. num .. ': longtable head not found')
  end
  local head = tex:sub(h1 + 1, e0 - 1)
  local cont = '\\multicolumn{' .. #tbl.colspecs .. '}{@{}l@{}}{\\textbf{Table '
    .. num .. '} (continued)}\\\\\n' .. top .. head .. '\\endhead'
  tex = tex:sub(1, e0 - 1) .. '\\endfirsthead\n' .. cont .. tex:sub(e1 + 1)
  return pandoc.RawBlock('latex', (tex:gsub('%s+$', '')))
end

local function Pandoc(doc)
  local blocks = doc.blocks
  local out = pandoc.List()
  local i = 1
  while i <= #blocks do
    local b = blocks[i]
    local num, cap = table_caption(b)
    if num then
      -- caption must be followed by a table, optionally after one paragraph
      local t_idx
      if blocks[i + 1] and blocks[i + 1].t == 'Table' then t_idx = i + 1
      elseif blocks[i + 2] and blocks[i + 2].t == 'Table'
        and blocks[i + 1].t == 'Para' then t_idx = i + 2 end
      if not t_idx then
        fail('caption "Table ' .. num .. '" is not followed by a table')
      end
      out:insert(pandoc.RawBlock('latex',
        '\\ThesisTableCaption{' .. num .. '}{' .. latex_inlines(cap) .. '}'))
      if t_idx == i + 2 then
        -- the sub-label line directly under a caption is not indented
        local sub = blocks[i + 1]
        sub.content:insert(1, pandoc.RawInline('latex', '\\noindent '))
        out:insert(sub)
        out:insert(pandoc.RawBlock('latex', '\\nopagebreak'))
      end
      if num:match('^%u%.%d+$') then
        out:insert(continued_table(convert_table(blocks[t_idx]), num))
      else
        out:insert(convert_table(blocks[t_idx]))
      end
      i = t_idx + 1
    elseif b.t == 'Header' then
      out:insert(convert_header(b))
      i = i + 1
    elseif b.t == 'Table' then
      out:insert(convert_table(b))
      i = i + 1
    elseif b.t == 'Div' and b.classes:includes('tablenote') then
      out:insert(pandoc.RawBlock('latex', '\\begin{ThesisTableNote}'))
      out:extend(b.content)
      out:insert(pandoc.RawBlock('latex', '\\end{ThesisTableNote}'))
      i = i + 1
    else
      local cap_like = b.t == 'Para' and stringify(b):match('^Table %w+%.%d+ [—–]')
      if cap_like then
        fail('paragraph looks like a table caption but is not a bold caption line: '
          .. stringify(b):sub(1, 60))
      end
      out:insert(b)
      i = i + 1
    end
  end
  doc.blocks = out
  return doc
end

-- The inline pass runs first, so headings and captions (rendered to raw
-- LaTeX by the block pass) already carry the inline transformations.
return {
  inline_filter,
  { Pandoc = Pandoc },
}
