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

1. Python  kurulu olmalı.
2. Projeyi klonlayın:
   ```bash
   git clone https://github.com/aysenurarslann/task_manager_bot.git
   cd task_manager_bot
3. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt

## Ortam Değişkenlerini Ayarlama (PowerShell - Windows)
Botun çalışması için gerekli kimlik bilgilerini aşağıdaki gibi ayarlayın:

$env:DISCORD_BOT_TOKEN="buraya_discord_bot_tokeninizi_yazın"

$env:FUSION_BRAIN_KEY="buraya_fusion_brain_keyinizi_yazın"

$env:FUSION_BRAIN_SECRET="buraya_fusion_brain_secretinizi_yazın"

## Botu Başlatma
Ortam değişkenleri ayarlandıktan sonra botu başlatmak için terminalde şu komutu çalıştırın:
   ```bash
   python bot.py
   ```

## Testleri Çalıştırma
Testleri çalıştırmak için:
```bash
python run_tests.py
