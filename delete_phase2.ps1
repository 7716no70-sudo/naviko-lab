# Naviko System - 不要データ削除スクリプト Phase 2
# 実行場所: ローカルPC (C:\Users\7716n\OneDrive\デスクトップ\naviko)
# 作成日: 2026-07-05

# ===================================================================
# Phase 2: 中優先度削除（182KB）- テスト・バックアップ関連
# ===================================================================

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "🗑️  Naviko System - 不要データ削除スクリプト Phase 2" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# 作業ディレクトリに移動
$navikoPath = "C:\Users\7716n\OneDrive\デスクトップ\naviko\navikoLAB"
Set-Location $navikoPath

Write-Host "📍 作業ディレクトリ: $navikoPath" -ForegroundColor Yellow
Write-Host ""

# 削除前のサイズ確認
Write-Host "📊 削除前のサイズ確認..." -ForegroundColor Green
$beforeSize = (Get-ChildItem -Recurse | Measure-Object -Property Length -Sum).Sum / 1KB
Write-Host "   現在のサイズ: $([math]::Round($beforeSize, 2)) KB" -ForegroundColor White
Write-Host ""

# ===================================================================
# 削除対象リスト（中優先度）
# ===================================================================
$deleteTargets = @(
    @{Path="recovery_test"; Type="Directory"; Size="73KB"; Reason="リカバリーテスト用"},
    @{Path="restore_test"; Type="Directory"; Size="73KB"; Reason="リストアテスト用"},
    @{Path="backup_verification"; Type="Directory"; Size="12KB"; Reason="バックアップ検証テスト用"},
    @{Path="external_backup"; Type="Directory"; Size="13KB"; Reason="外部バックアップテスト用"},
    @{Path="run_integration_test.py"; Type="File"; Size="8KB"; Reason="統合テスト実行スクリプト"},
    @{Path="test_autonomous_core_capability_connection.py"; Type="File"; Size="3KB"; Reason="コア機能接続テスト"}
)

$successCount = 0
$notFoundCount = 0

foreach ($target in $deleteTargets) {
    $index = $deleteTargets.IndexOf($target) + 1
    $total = $deleteTargets.Count
    
    Write-Host "🟡 [$index/$total] $($target.Path) を削除中..." -ForegroundColor Yellow
    Write-Host "   理由: $($target.Reason) ($($target.Size))" -ForegroundColor Gray
    
    if (Test-Path $target.Path) {
        if ($target.Type -eq "Directory") {
            Remove-Item $target.Path -Recurse -Force
        } else {
            Remove-Item $target.Path -Force
        }
        Write-Host "   削除完了: ✅" -ForegroundColor Green
        $successCount++
    } else {
        Write-Host "   ⚠️  見つかりません（既に削除済み）" -ForegroundColor Yellow
        $notFoundCount++
    }
    Write-Host ""
}

# 削除後のサイズ確認
Write-Host "📊 削除後のサイズ確認..." -ForegroundColor Green
$afterSize = (Get-ChildItem -Recurse | Measure-Object -Property Length -Sum).Sum / 1KB
$deletedSize = $beforeSize - $afterSize
Write-Host "   削除後のサイズ: $([math]::Round($afterSize, 2)) KB" -ForegroundColor White
Write-Host "   削減サイズ: $([math]::Round($deletedSize, 2)) KB" -ForegroundColor Cyan
Write-Host ""

Write-Host "📈 削除サマリー:" -ForegroundColor Cyan
Write-Host "   成功: $successCount 件" -ForegroundColor Green
Write-Host "   見つからず: $notFoundCount 件" -ForegroundColor Yellow
Write-Host "   合計: $($deleteTargets.Count) 件" -ForegroundColor White
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
git commit -m "refactor: テスト・バックアップ関連ファイル削除 Phase 2 (182KB削減)

削除内容:
- recovery_test/ (リカバリーテスト)
- restore_test/ (リストアテスト)
- backup_verification/ (バックアップ検証)
- external_backup/ (外部バックアップ)
- run_integration_test.py (統合テスト)
- test_autonomous_core_capability_connection.py (接続テスト)

合計182KB削減"

Write-Host ""
Write-Host "🚀 GitHub にプッシュ..." -ForegroundColor Yellow
git push origin main

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "✅ Phase 2 完了！" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "次のステップ:" -ForegroundColor Cyan
Write-Host "1. Workspace側で git pull を実行" -ForegroundColor White
Write-Host "2. Phase 3（低優先度1.3MB調査）を実施するか判断" -ForegroundColor White
Write-Host ""
Write-Host "累積削減サイズ: 56MB (Phase 1) + 182KB (Phase 2) = 約56.2MB" -ForegroundColor Yellow
Write-Host ""
