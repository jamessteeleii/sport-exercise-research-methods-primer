-- Format each chapter independently, including citations in its notes. This
-- prevents book-wide disambiguation and puts the bibliography beside its text.
local function chapter(blocks, meta, slug)
  local notes = pandoc.List()
  local section = pandoc.Pandoc(blocks, meta)
  -- HTML collects notes before its bibliography; PDF/Word retain native
  -- footnotes, so the typesetter places them on the page of their markers.
  if FORMAT:match('html') then
  section = section:walk({Note = function(note)
    local n = #notes + 1
    local id = slug .. '-note-' .. n
    local marker = slug .. '-noteref-' .. n
    local contents = note.content
    contents:insert(pandoc.Plain({pandoc.Link({pandoc.Str('↩')}, '#' .. marker,
      'Return to text', pandoc.Attr('', {}, {['aria-label']='Return to footnote ' .. n}))}))
    notes:insert(pandoc.Div(contents, pandoc.Attr(id, {'chapter-note'})))
    return pandoc.Span({pandoc.Superscript({pandoc.Link({pandoc.Str(tostring(n))}, '#' .. id)})},
      pandoc.Attr(marker, {'chapter-noteref'}))
  end})
  if #notes > 0 then
    section.blocks:insert(pandoc.Header(2, 'Footnotes', pandoc.Attr(slug .. '-footnotes', {'unnumbered'})))
    local items = pandoc.List()
    for _, note in ipairs(notes) do items:insert({note}) end
    section.blocks:insert(pandoc.Div({pandoc.OrderedList(items)}, pandoc.Attr('', {'chapter-footnotes'})))
  end
  end
  local has_citations = false
  section:walk({Cite=function() has_citations = true end})
  if has_citations then
    section.blocks:insert(pandoc.Header(2, 'References', pandoc.Attr(slug .. '-references', {'unnumbered'})))
    section.blocks:insert(pandoc.Div({}, pandoc.Attr('refs')))
    section.meta['suppress-bibliography'] = false
    section.meta['reference-section-title'] = ''
    section = pandoc.utils.citeproc(section)
    -- IDs must remain unique in the merged PDF and citations must stay local
    -- to their chapter even when another chapter cites the same source.
    section = section:walk({
      Cite=function(el) return el.content end,
      Div=function(el)
        if el.identifier == 'refs' or el.identifier:match('^ref%-') then
          el.identifier = slug .. '-' .. el.identifier
        end
        return el
      end,
      Link=function(el)
        if el.target:match('^#ref%-') then
          el.target = '#' .. slug .. '-' .. el.target:sub(2)
          el.attributes['role'] = 'doc-biblioref'
        end
        return el
      end
    })
  end
  return section.blocks
end

function Pandoc(doc)
  local out, current = pandoc.List(), pandoc.List()
  local slug, serial = 'frontmatter', 0
  local function flush()
    if #current > 0 then out:extend(chapter(current, doc.meta, slug)) end
    current = pandoc.List()
  end
  for _, block in ipairs(doc.blocks) do
    if block.t == 'Header' and block.level == 1 then
      flush()
      serial = serial + 1
      slug = block.identifier ~= '' and block.identifier or ('section-' .. serial)
    end
    current:insert(block)
  end
  flush()
  doc.blocks = out
  return doc
end
