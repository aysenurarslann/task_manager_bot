import discord
from discord.ext import commands
import os
import requests
import json
import time
import base64

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def fusion_pipeline():
    key = os.getenv("FUSION_BRAIN_KEY")
    secret = os.getenv("FUSION_BRAIN_SECRET")
    if not key or not secret:
        raise ValueError("Fusion Brain API anahtarları eksik.")
    headers = {
        "X-Key": f"Key {key}",
        "X-Secret": f"Secret {secret}"
    }
    response = requests.get(
        "https://api-key.fusionbrain.ai/key/api/v1/pipelines",
        headers=headers,
        timeout=10
    )
    if response.status_code != 200:
        raise RuntimeError(f"Pipeline alınamadı: {response.status_code}")
    pipelines = response.json()
    return pipelines[0]["id"]

def start_fusion_gen(prompt, pipeline_id):
    key = os.getenv("FUSION_BRAIN_KEY")
    secret = os.getenv("FUSION_BRAIN_SECRET")
    headers = {
        "X-Key": f"Key {key}",
        "X-Secret": f"Secret {secret}"
    }
    params = {
        "type": "GENERATE",
        "numImages": 1,
        "width": 512,
        "height": 512,
        "generateParams": {
            "query": prompt
        }
    }
    data = {
        "pipeline_id": (None, pipeline_id),
        "params": (None, json.dumps(params), "application/json")
    }
    response = requests.post(
        "https://api-key.fusionbrain.ai/key/api/v1/pipeline/run",
        headers=headers,
        files=data,
        timeout=30
    )
    if response.status_code not in (200, 201):
       raise RuntimeError(f"Görev başlatılamadı: {response.status_code}")
    result = response.json()
    return result["uuid"]

def wait_for_fusion_img(uuid):
    key = os.getenv("FUSION_BRAIN_KEY")
    secret = os.getenv("FUSION_BRAIN_SECRET")
    headers = {
        "X-Key": f"Key {key}",
        "X-Secret": f"Secret {secret}"
    }
    for _ in range(20):
        time.sleep(2)
        response = requests.get(
            f"https://api-key.fusionbrain.ai/key/api/v1/pipeline/status/{uuid}",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "DONE":
                return data["result"]["files"][0]
            elif data["status"] == "FAIL":
                raise RuntimeError("Görsel üretim başarısız.")
    raise RuntimeError("Görsel üretim zaman aşımına uğradı.")

@bot.event
async def on_ready():
    from database import init_db
    init_db()
    print(f"{bot.user} olarak giriş yapıldı.")

@bot.command(name="add_task")
async def add_task_cmd(ctx, *, description: str):
    if not description.strip():
        await ctx.send("Görev açıklaması boş olamaz.")
        return
    from database import add_task
    task_id = add_task(description)
    await ctx.send(f"Görev eklendi! ID: {task_id} , Tüm görevleri görmek için `!show_tasks` komutunu kullanabilirsiniz.")

@bot.command(name="delete_task")
async def delete_task_cmd(ctx, task_id: int):
    from database import delete_task
    if delete_task(task_id):
        await ctx.send(f"Görev #{task_id} silindi.")
    else:
        await ctx.send(f"Görev #{task_id} bulunamadı.")

@bot.command(name="show_tasks")
async def show_tasks_cmd(ctx):
    from database import get_all_tasks
    tasks = get_all_tasks()
    if not tasks:
        await ctx.send("Hiç görev yok.")
        return
    lines = ["**Görevlerin listesi:**"]
    for t in tasks:
        mark = "✅" if t["completed"] else "⏳"
        lines.append(f"{mark} #{t['id']}: {t['description']}")
    
    await ctx.send("\n".join(lines))

@bot.command(name="complete_task")
async def complete_task_cmd(ctx, task_id: int):
    from database import complete_task
    if complete_task(task_id):
        await ctx.send(f"Görev #{task_id} tamamlandı!")
        await ctx.send(f"Harika iş çıkardın, <@{ctx.author.id}>! 🎉")
    else:
        await ctx.send(f"Görev #{task_id} zaten tamamlanmış ya da mevcut değil.")

@bot.command(name="celebrate")
async def celebrate_cmd(ctx, task_id: int):
    from database import is_task_completed, get_all_tasks
    if not is_task_completed(task_id):
        await ctx.send(f"Görev #{task_id} henüz tamamlanmamış.")
        return

    tasks = get_all_tasks()
    desc = next((t["description"] for t in tasks if t["id"] == task_id), "Bilinmeyen görev")

    try:
        pipeline = fusion_pipeline()
        prompt = f"Minimalist celebration badge for completing: '{desc}'. Symbolic, clean, no text, no letters, flat design, vibrant colors"
        uuid = start_fusion_gen(prompt, pipeline)
        image_b64 = wait_for_fusion_img(uuid)
        os.makedirs("images", exist_ok=True)
        path = f"images/celebration_{task_id}.png"
        with open(path, "wb") as f:
            f.write(base64.b64decode(image_b64))
        await ctx.send(f"🎉 Görev tamamlandı: **{desc}**")
        await ctx.send(file=discord.File(path))
    except Exception as e:
        await ctx.send(f"Görsel üretilirken hata oluştu: {str(e)}")

if __name__ == "__main__":
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("HATA: DISCORD_BOT_TOKEN ortam değişkeni ayarlanmamış.")
    else:
        bot.run(token)