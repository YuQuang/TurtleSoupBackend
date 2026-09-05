## Flask 範例

啟動前請在 `.env` 設定 PostgreSQL 連線資訊，使用其中一種格式：

```dotenv
DATABASE_URL=postgresql://user:password@localhost:5432/turtlesoup
```

或：

```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=turtlesoup
DB_USER=user
DB_PASSWORD=password
```

安裝依賴並啟動開發伺服器：

```powershell
uv run python -m turtlesoup.app
```

伺服器啟動後，可使用以下 `POST` endpoint：

```powershell
Invoke-RestMethod `
	-Uri http://127.0.0.1:5000/api/messages `
	-Method Post `
	-ContentType "application/json" `
	-Body '{"message":"Hello Flask"}'
```

成功回應的 HTTP status 為 `201`：

```json
{
	"message": "Hello Flask",
	"status": "created"
}
```
