# チャットのCRUD: Create(作成) / Read(読み取り) / Update(更新) / Delete(削除)

from marketinsight_history.client import container

# ユーザーの全チャットをCosmosDBから取得する
def get_chats(user_id: str):
    query = "SELECT * FROM c WHERE c.user_id = @user_id ORDER BY c.date DESC"
    params = [{"name": "@user_id", "value": user_id}]
    return list(container.query_items(query=query, parameters=params, partition_key=user_id))

# 新しいチャットデータをCosmosDBに保存する
def create_chat(user_id: str, chat_id: str, title: str, date: str):
    container.upsert_item({
        "id": chat_id,
        "user_id": user_id,
        "title": title,
        "date": date,
        "favorite": False,
        "messages": [],
    })

# チャットをCosmosDBから削除する
def delete_chat(user_id: str, chat_id: str):
    container.delete_item(item=chat_id, partition_key=user_id)

# お気に入りのOn/Offを切り替える
def toggle_favorite(user_id: str, chat_id: str):
    chat = container.read_item(item=chat_id, partition_key=user_id)
    chat["favorite"] = not chat["favorite"]
    container.upsert_item(chat)

# チャットのタイトルを変更する
def update_title(user_id: str, chat_id: str, title: str):
    chat = container.read_item(item=chat_id, partition_key=user_id)
    chat["title"] = title
    container.upsert_item(chat)

# チャットにメッセージを追加する
def add_message(user_id: str, chat_id: str, role: str, content: str):
    chat = container.read_item(item=chat_id, partition_key=user_id)
    chat["messages"].append({"role": role, "content": content})
    container.upsert_item(chat)

# チャットの会話履歴を取得する
def get_messages(user_id: str, chat_id: str):
    chat = container.read_item(item=chat_id, partition_key=user_id)
    return [{"role": m["role"], "content": m["content"]} for m in chat.get("messages", [])]