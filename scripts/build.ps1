[CmdletBinding()]
param(
  [ValidateSet('web','pdf','review','all')][string]$Target='web',
  [string]$Python='python'
)
$ErrorActionPreference='Stop'
$bookRoot=Split-Path $PSScriptRoot -Parent
Push-Location -LiteralPath $bookRoot
try {
  & $Python scripts/sync_metadata.py
  if ($LASTEXITCODE -ne 0) { throw 'Citation metadata validation failed.' }
  & $Python scripts/chapter_bibliographies.py
  if ($LASTEXITCODE -ne 0) { throw 'Chapter bibliography generation failed.' }
  if ($Target -in @('web','all')) {
    & quarto render --to all
    if ($LASTEXITCODE -ne 0) { throw 'Book rendering failed.' }
  } elseif ($Target -eq 'pdf') {
    & quarto render --to typst
    if ($LASTEXITCODE -ne 0) { throw 'PDF rendering failed.' }
  }
  if ($Target -in @('review','all')) {
    & quarto render --profile review --to docx
    if ($LASTEXITCODE -ne 0) { throw 'Whole-book Word rendering failed.' }
    New-Item -ItemType Directory -Force '_review/chapters' | Out-Null
    $publication=Get-Content -LiteralPath 'config/publication.json' -Raw | ConvertFrom-Json
    foreach ($chapter in $publication.chapters) {
      $chapterStem=[IO.Path]::GetFileNameWithoutExtension($chapter.file)
      & quarto pandoc $chapter.file --from=markdown --to=docx --standalone '--resource-path=chapters;.' --citeproc "--bibliography=bibliography/chapters/$chapterStem.bib" --csl=bibliography/apa.csl --metadata=link-citations:true --metadata=reference-section-title:References --lua-filter=scripts/book-formatting.lua --reference-doc=assets/review-reference.docx --output="_review/chapters/$chapterStem.docx"
      if ($LASTEXITCODE -ne 0) { throw "Word rendering failed for $chapterStem" }
    }
  }
  & $Python scripts/validate.py
  if ($LASTEXITCODE -ne 0) { throw 'Project checks failed.' }
} finally { Pop-Location }
