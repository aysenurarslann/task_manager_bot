# Küçük Ekip Görev Yönetimi Botu

Bu proje, küçük ekipler için Discord üzerinden görev yönetimi sağlayan bir bottur.

## Özellikler

- `!add_task <açıklama>`: Yeni görev ekler.
- `!delete_task <id>`: Belirtilen ID’deki görevi siler.
- `!show_tasks`: Tüm görevleri listeler.
- `!complete_task <id>`: Görevi tamamlandı olarak işaretler.
- `!celebrate <id>`: Tamamlanan görev için kutlama görseli üretir ve gönderir.

Veriler yerel bir SQLite veritabanında saklanır.

## Kurulum

1. Python 3.8+ kurulu olmalı.
2. Projeyi klonlayın:
   ```bash
   git clone https://github.com/sizin-kullanici-adi/task_manager_bot.git
   cd task_manager_bot