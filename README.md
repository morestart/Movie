# 上映电影插件

## 使用方法：

- 将movie.py放于`homeassistant\components`下
- `scheduler.add_job(restart_ha, 'cron', day_of_week='0', hour=2, minute=00)`
在此行更改movie插件的显示时间
- 关于APScheduler的时间更改
- 修改`os.system("curl -d \"\" http://192.168.0.102:8123/api/services/homeassistant/restart?api_password=HA密码")`此处密码

## 配置内容:

conf下写入此行
```yaml
movie:
```