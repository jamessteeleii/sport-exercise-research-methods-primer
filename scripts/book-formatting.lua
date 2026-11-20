-- Shared presentation only. Author prose, citations and review decisions stay intact.
function Header(el)
  el.classes:insert('unnumbered')
  return el
end

function Table(el)
  local header = pandoc.utils.stringify(el.head)
  if #el.colspecs == 5 and header:match('Topic') and header:match('Problem')
      and header:match('Objectives') then
    local widths = {0.14, 0.22, 0.20, 0.20, 0.24}
    for i, width in ipairs(widths) do
      el.colspecs[i][2] = width
    end
  end
  if FORMAT:match('html') then
    return pandoc.Div({el}, pandoc.Attr('', {'table-responsive'}))
  end
  return el
end

function Span(el)
  if el.classes:includes('mark') or el.classes:includes('Estilo4') then
    return el.content
  end
end

function Div(el)
  if el.classes:includes('quote-attribution') then
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
    return {pandoc.RawBlock('typst', '#text(size: 9pt)['), el,
            pandoc.RawBlock('typst', ']')}
  end
end

local function caption(block)
  if block.t ~= 'Para' or not block.content[1] or block.content[1].t ~= 'Strong' then return false end
  return pandoc.utils.stringify(block.content[1]):match('^Figure %d+%.$')
      or pandoc.utils.stringify(block.content[1]):match('^Table %d+%.$')
end

function Blocks(blocks)
  local out = pandoc.List()
  for _, block in ipairs(blocks) do
    if caption(block) then
      out:insert(pandoc.Div({block}, pandoc.Attr('', {'book-caption'})))
    else
      out:insert(block)
    end
  end
  return out
end
