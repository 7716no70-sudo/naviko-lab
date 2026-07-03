# Naviko LAB ユーザーガイド v1.4.0

## Navikoとは

**自分で考えて成長するAI**

### 最終目的
「製作者がPC上で行える作業は、製作者が許可すればナビ子にもできる」

### 理想の動作
あなた: 「プレゼン資料を作成して」
Naviko: 自分で判断→調査→作成→完成

---

## インストール
git clone https://github.com/7716no70-sudo/naviko-lab.git
cd naviko-lab
pip install -r requirements.txt

## 使い方
from navikoLAB.app_project_builder import AppProjectBuilder
builder = AppProjectBuilder(lab_dir=lab_dir)
result = builder.build_basic_app_project(purpose='計算機', project_name='calc')

---
バージョン: v1.4.0
設計思想: 自分で考えて成長するAI
