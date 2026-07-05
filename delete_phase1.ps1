# Naviko System - 不要データ削除スクリプト
# 実行場所: ローカルPC (C:\Users\7716n\OneDrive\デスクトップ\naviko)
# 作成日: 2026-07-05

# ===================================================================
# Phase 1: 高優先度削除（56MB）
# ===================================================================

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "🗑️  Naviko System - 不要データ削除スクリプト Phase 1" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# 作業ディレクトリに移動
$navikoPath = "C:\Users\7716n\OneDrive\デスクトップ\naviko\navikoLAB"
Set-Location $navikoPath

Write-Host "📍 作業ディレクトリ: $navikoPath" -ForegroundColor Yellow
Write-Host ""

# 削除前のサイズ確認
Write-Host "📊 削除前のサイズ確認..." -ForegroundColor Green
$beforeSize = (Get-ChildItem -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
Write-Host "   現在のサイズ: $([math]::Round($beforeSize, 2)) MB" -ForegroundColor White
Write-Host ""

# ===================================================================
# 削除対象1: python-manager-26.3.msix (45MB)
# ===================================================================
Write-Host "🔴 [1/2] python-manager-26.3.msix を削除中..." -ForegroundColor Red
$file1 = "python-manager-26.3.msix"

if (Test-Path $file1) {
    $size1 = (Get-Item $file1).Length / 1MB
    Write-Host "   ファイル確認: ✅ 存在（$([math]::Round($size1, 2)) MB）" -ForegroundColor Green
    Remove-Item $file1 -Force
    Write-Host "   削除完了: ✅" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  ファイルが見つかりません" -ForegroundColor Yellow
}
Write-Host ""

# ===================================================================
# 削除対象2: docs/auto_documentation_20260626_211640.md (11MB)
# ===================================================================
Write-Host "🔴 [2/2] docs/auto_documentation_20260626_211640.md を削除中..." -ForegroundColor Red
$file2 = "docs\auto_documentation_20260626_211640.md"

if (Test-Path $file2) {
    $size2 = (Get-Item $file2).Length / 1MB
    Write-Host "   ファイル確認: ✅ 存在（$([math]::Round($size2, 2)) MB）" -ForegroundColor Green
    Remove-Item $file2 -Force
    Write-Host "   削除完了: ✅" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  ファイルが見つかりません" -ForegroundColor Yellow
}
Write-Host ""

# 削除後のサイズ確認
Write-Host "📊 削除後のサイズ確認..." -ForegroundColor Green
$afterSize = (Get-ChildItem -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
$deletedSize = $beforeSize - $afterSize
Write-Host "   削除後のサイズ: $([math]::Round($afterSize, 2)) MB" -ForegroundColor White
Write-Host "   削減サイズ: $([math]::Round($deletedSize, 2)) MB" -ForegroundColor Cyan
Write-Host ""

# ===================================================================
# Git コミット & プッシュ
# ===================================================================
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "📦 Git コミット & プッシュ" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

Set-Location "C:\Users\7716n\OneDrive\デスクトップ\naviko"

Write-Host "🔍 Git状態確認..." -ForegroundColor Yellow
git status

Write-Host ""
Write-Host "📝 削除をステージング..." -ForegroundColor Yellow
git add -A

Write-Host ""
Write-Host "💾 コミット作成..." -ForegroundColor Yellow
git commit -m "refactor: 開発用不要ファイル削除 Phase 1 (56MB削減)

- python-manager-26.3.msix (45MB) 削除
- docs/auto_documentation_20260626_211640.md (11MB) 削除
- 合計56MB削減
- navikoLABサイズ: 60MB → 4MB"

Write-Host ""
Write-Host "🚀 GitHub にプッシュ..." -ForegroundColor Yellow
git push origin main

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "✅ Phase 1 完了！" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "次のステップ:" -ForegroundColor Cyan
Write-Host "1. Workspace側で git pull を実行" -ForegroundColor White
Write-Host "2. Phase 2（中優先度182KB削除）を実行する場合は Phase2スクリプトを実行" -ForegroundColor White
Write-Host ""
Write-Host "Phase 2スクリプト: .\delete_phase2.ps1" -ForegroundColor Yellow
Write-Host ""
