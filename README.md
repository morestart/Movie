# 豆瓣电影

## 使用方法：

- 将movie.py放于`homeassistant\components`下
- `scheduler.add_job(restart_ha, 'cron', day_of_week='0', hour=2, minute=00)`
在此行更改movie插件的显示时间
- 关于APScheduler的时间更改

    >minute:表示分钟，可以是从0到59之间的任何整数。
    >
    >hour:表示小时，可以是从0到23之间的任何整数。
    >
    >day:表示日期，可以是从1到31之间的任何整数。
    >
    >month:表示月份，可以是从1到12之间的任何整数。
    >
    >week:表示星期几，可以是从0到7之间的任何整数，这里的0或7代表星期日。
    >星号(*):代表所有可能的值，例如month字段如果是星号，则表示在满足其它字段的制约条件后每月都执行该命令操作。
    >
    >逗号(,):可以用逗号隔开的值指定一个列表范围，例如，“1,2,5,7,8,9”
    >
    >中杠(-):可以用整数之间的中杠表示一个整数范围，例如“2-6”表示“2,3,4,5,6”
    >
    >正斜线(/):可以用正斜线指定时间的间隔频率，例如“0-23/2”表示每两小时执行一次。同时正斜线可以和星号一起使用，例如*/10，
    >
    >如果用在minute字段，表示每十分钟执行一次。
- 修改`os.system("curl -d \"\" http://192.168.0.102:8123/api/services/homeassistant/restart?api_password=HA密码")`此处密码

## 配置内容:

conf下写入此行
```yaml
movie:
```