-- Shared presentation only. Author prose, citations and review decisions stay intact.
function Image(el)
  if FORMAT:match('docx') and el.src:match('figure%-crops/') then
    -- Word reading proofs use the original raster figures. The SVG viewport
    -- derivatives are for HTML/PDF and otherwise require an external converter.
    local file = assert(io.open('config/figure-crops.json', 'r'))
    local crops = pandoc.json.decode(file:read('*a'))
    file:close()
    for _, crop in ipairs(crops) do
      if el.src == crop.derivative then el.src = crop.source; return el end
      if el.src == '../' .. crop.derivative then el.src = '../' .. crop.source; return el end
    end
    error('No original raster figure recorded for ' .. el.src)
  end
  return el
end

function Header(el)
  el.classes:insert('unnumbered')
  return el
end

function Table(el)
  local header = ''
  local function row_text(row)
    if not row then return '' end
    local parts = {}
    for _, cell in ipairs(row.cells) do table.insert(parts, pandoc.utils.stringify(pandoc.Div(cell.contents))) end
    return table.concat(parts, ' ')
  end
  for _, row in ipairs(el.head.rows) do header = header .. row_text(row) .. ' ' end
  if el.bodies[1] then header = header .. row_text(el.bodies[1].body[1]) end
  -- Two imported layout tables are breakout boxes, not numbered data tables.
  if header:match('conducted a literature review') or header:match('What are AI models') then
    local blocks = pandoc.List()
    for _, body in ipairs(el.bodies) do
      for _, row in ipairs(body.body) do
        for _, cell in ipairs(row.cells) do blocks:extend(cell.contents) end
      end
    end
    return pandoc.Div(blocks, pandoc.Attr('', {'book-box'}))
  end
  local title
  if header:match('^PrimaryEvidence') and #el.head.rows == 0 then
    -- Word split chapter nine's Table 1 into two adjacent table objects.
    -- Retain its continuation and repeat the same column headings.
    local headings = el.bodies[1].body[1]:clone()
    for i, label in ipairs({'', 'Primary Purpose', 'Example'}) do
      headings.cells[i].contents = {pandoc.Plain({pandoc.Str(label)})}
    end
    table.insert(el.head.rows, headings)
    title = {pandoc.Para({pandoc.Str('Table 1 (continued). Different types of figures to visualize data')})}
    header = 'Primary Purpose ' .. header
  end
  -- Pandoc's native captions must be retained too, not only imported title rows.
  if el.caption and #el.caption.long > 0 then
    title = el.caption.long
    el.caption.long = {}
    el.caption.short = nil
  end
  if #el.head.rows == 1 and #el.head.rows[1].cells == 1 then
    local cell = el.head.rows[1].cells[1]
    if cell.col_span == #el.colspecs and pandoc.utils.stringify(pandoc.Div(cell.contents)):match('^Table %d+%.') then
      title = cell.contents
      el.head.rows = {}
    end
  end
  -- Restore the two-level headings in the design and Anscombe comparison tables.
  if header:match('Types of Questions:') and #el.head.rows == 1 then
    table.insert(el.head.rows, table.remove(el.bodies[1].body, 1))
  elseif header:match('Dataset A') and #el.head.rows == 0 then
    table.insert(el.head.rows, table.remove(el.bodies[1].body, 1))
    table.insert(el.head.rows, table.remove(el.bodies[1].body, 1))
  elseif header:match('^Truth') and #el.head.rows == 0 then
    table.insert(el.head.rows, table.remove(el.bodies[1].body, 1))
  elseif header:match('^Quantitative') and #el.head.rows == 0 then
    -- These labels shared a cell with lists; retain those lists in the body.
    local row = el.bodies[1].body[1]
    local headings = row:clone()
    for i, cell in ipairs(row.cells) do
      headings.cells[i].contents = {cell.contents[1]}
      table.remove(cell.contents, 1)
    end
    table.insert(el.head.rows, headings)
  elseif (header:match('^Thematic Narrative Analysis') or header:match('^Autoethnography')) and #el.head.rows == 0 then
    local headings = el.bodies[1].body[1]:clone()
    headings.cells[1].contents = {pandoc.Plain({pandoc.Str('Analysis')})}
    headings.cells[2].contents = {pandoc.Plain({pandoc.Str('Focus')})}
    table.insert(el.head.rows, headings)
  end
  -- Several imported tables had their real column headings in the body.
  -- Promote only short, wholly emphasised label rows; leave prose cells intact.
  if #el.head.rows == 0 and #el.bodies > 0 and #el.bodies[1].body > 0 then
    local row = el.bodies[1].body[1]
    local labels = true
    for _, cell in ipairs(row.cells) do
      local txt = pandoc.utils.stringify(pandoc.Div(cell.contents))
      if #cell.contents > 1 or #txt > 90 then labels = false end
      if txt ~= '' then
        local strong = false
        pandoc.Div(cell.contents):walk({Strong=function() strong=true end})
        if not strong then labels=false end
      end
    end
    if labels then
      table.insert(el.head.rows, row)
      table.remove(el.bodies[1].body, 1)
    end
  end
  if #el.colspecs == 5 and header:match('Topic') and header:match('Problem')
      and header:match('Objectives') then
    local widths = {0.14, 0.22, 0.20, 0.20, 0.24}
    for i, width in ipairs(widths) do
      el.colspecs[i][2] = width
    end
  end
  if #el.colspecs == 3 and (header:match('Primary Purpose') or header:match('Primary Evidence')) then
    for i, width in ipairs({0.13, 0.52, 0.35}) do el.colspecs[i][2] = width end
  end
  if #el.colspecs == 4 and header:match('Publication') and header:match('Journal') then
    for i, width in ipairs({0.15, 0.27, 0.10, 0.48}) do el.colspecs[i][2] = width end
  end
  if #el.colspecs == 4 and header:match('Possible research questions') then
    -- Imported widths left the Type column too narrow even for its heading.
    for i, width in ipairs({0.16, 0.29, 0.28, 0.27}) do el.colspecs[i][2] = width end
  end
  local content = pandoc.List()
  if title then content:insert(pandoc.Div(title, pandoc.Attr('', {'book-caption', 'table-caption'}))) end
  content:insert(el)
  if FORMAT:match('html') then
    return pandoc.Div(content, pandoc.Attr('', {'table-responsive'}, {tabindex='0', role='region', ['aria-label']='Scrollable table'}))
  end
  local classes = pandoc.List({'book-table'})
  if #el.colspecs >= 5 and #el.colspecs ~= 8 then classes:insert('book-table-landscape') end
  local rows = #el.head.rows
  for _, body in ipairs(el.bodies) do rows = rows + #body.body end
  if rows <= 6 and #pandoc.utils.stringify(pandoc.Div(content)) < 1500 then classes:insert('book-table-compact') end
  return pandoc.Div(content, pandoc.Attr('', classes))
end

function Span(el)
  if el.classes:includes('mark') or el.classes:includes('Estilo4') then
    return el.content
  end
end

function Div(el)
  if el.classes:includes('book-table-landscape') and FORMAT:match('typst') then
    return {pandoc.RawBlock('typst', '#page(flipped: true, margin: (x: 18mm, y: 20mm))[\n#show table: set text(size: 9.5pt)\n'), el, pandoc.RawBlock('typst', ']')}
  elseif el.classes:includes('book-table-compact') and FORMAT:match('typst') then
    return {pandoc.RawBlock('typst', '#block(width: 100%, breakable: false, above: 10pt, below: 10pt)['), el, pandoc.RawBlock('typst', ']')}
  elseif el.classes:includes('quote-attribution') then
    if FORMAT:match('typst') then
      return {pandoc.RawBlock('typst', '#align(right)['), el,
              pandoc.RawBlock('typst', ']')}
    elseif FORMAT:match('docx') then
      el.attributes['custom-style'] = 'Quote Attribution'
      return el
    end
  elseif el.classes:includes('book-box') and FORMAT:match('typst') then
    return {pandoc.RawBlock('typst', '#block(width: 100%, fill: rgb("f0f5eb"), stroke: rgb("ccd9bf"), inset: 12pt, breakable: true)['),
            el, pandoc.RawBlock('typst', ']')}
  elseif el.classes:includes('book-caption') and FORMAT:match('typst') then
    local sticky = el.classes:includes('table-caption') and 'true' or 'false'
    return {pandoc.RawBlock('typst', '#block(width: 100%, fill: rgb("f2f5ee"), inset: 8pt, above: 6pt, below: 8pt, sticky: ' .. sticky .. ', breakable: false)[#set text(size: 9pt)\n#set par(justify: false, leading: 0.5em)\n'), el,
            pandoc.RawBlock('typst', ']')}
  end
end

local function caption(block)
  if block.t ~= 'Para' or not block.content[1] or block.content[1].t ~= 'Strong' then return false end
  return pandoc.utils.stringify(block.content[1]):match('^Figure %d+%.$')
      or pandoc.utils.stringify(block.content[1]):match('^Table %d+%.$')
end

-- Caption numbers remain local to their chapter, as in the authors' drafts.
-- Explicit Markdown links in the maintained sources target these unique anchors
-- in both HTML and PDF. Do not automatically link external/example table numbers.
local function caption_targets(doc)
  local chapters = {
    ['sec-foundations']='ch01', ['sec-question-and-design']='ch02',
    ['sec-participants']='ch03', ['sec-quantitative-data-collection']='ch04',
    ['sec-quantitative-analysis']='ch05', ['sec-interviewing']='ch06',
    ['sec-qualitative-analysis']='ch07', ['sec-secondary-research']='ch08',
    ['sec-writing-and-peer-review']='ch09'
  }
  -- HTML books move the chapter H1 into the title block before user filters.
  local input = (quarto and quarto.doc.input_file) or PANDOC_STATE.input_files[1] or ''
  local slug = input:match('(%d%d)%-')
  if slug then slug = 'ch' .. slug end
  local out = pandoc.List()
  for _, block in ipairs(doc.blocks) do
    if block.t == 'Header' and block.level == 1 then slug = chapters[block.identifier] end
    if slug then
      block = block:walk({Strong=function(el)
        local kind, number = pandoc.utils.stringify(el):match('^(%a+) (%d+)%.')
        if kind == 'Table' or kind == 'Figure' then
          return pandoc.Span({el}, pandoc.Attr(kind:lower() .. '-' .. slug .. '-' .. number))
        end
      end})
    end
    out:insert(block)
  end
  doc.blocks = out
  return doc
end

function Blocks(blocks)
  local out = pandoc.List()
  local i = 1
  while i <= #blocks do
    local block = blocks[i]
    local nextblock = blocks[i + 1]
    local imagepara = block.t == 'Para' and #block.content == 1 and block.content[1].t == 'Image'
    if caption(block) and nextblock and nextblock.t == 'Div' and
        (nextblock.classes:includes('book-table') or nextblock.classes:includes('table-responsive')) then
      nextblock.content:insert(1, pandoc.Div({block}, pandoc.Attr('', {'book-caption', 'table-caption'})))
      out:insert(nextblock)
      i = i + 2
    elseif caption(block) and pandoc.utils.stringify(block):match('^Table ') and nextblock and
        nextblock.t == 'Para' and #nextblock.content == 1 and nextblock.content[1].t == 'Image' then
      if FORMAT:match('typst') then out:insert(pandoc.RawBlock('typst', '#block(width: 100%, breakable: false, above: 12pt, below: 12pt)[')) end
      out:insert(pandoc.Div({block}, pandoc.Attr('', {'book-caption', 'table-caption'})))
      out:insert(nextblock)
      if FORMAT:match('typst') then out:insert(pandoc.RawBlock('typst', ']')) end
      i = i + 2
    elseif imagepara and nextblock and caption(nextblock) then
      local cap = pandoc.Div({nextblock}, pandoc.Attr('', {'book-caption'}))
      if FORMAT:match('typst') then
        out:insert(pandoc.RawBlock('typst', '#block(width: 100%, breakable: false, above: 12pt, below: 12pt)[\n#align(center)['))
        out:insert(block)
        out:insert(pandoc.RawBlock('typst', ']'))
        out:insert(cap)
        out:insert(pandoc.RawBlock('typst', ']'))
      else
        out:insert(pandoc.Div({block, cap}, pandoc.Attr('', {'book-figure'})))
      end
      i = i + 2
    elseif imagepara and FORMAT:match('typst') then
      out:insert(pandoc.RawBlock('typst', '#align(center)['))
      out:insert(block)
      out:insert(pandoc.RawBlock('typst', ']'))
      i = i + 1
    else
    if caption(block) then
      out:insert(pandoc.Div({block}, pandoc.Attr('', {'book-caption'})))
    else
      out:insert(block)
    end
    i = i + 1
    end
  end
  return out
end

-- Run grouping before styling so newly formed caption divs receive PDF styles.
return {{Image=Image, Header=Header, Table=Table, Span=Span}, {Blocks=Blocks}, {Div=Div}, {Pandoc=caption_targets}}
