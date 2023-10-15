# Простая Atomic-based CI/CD система

*Disclamer:*
```
Это демо проект CI системы, на которой в курсе "Обеспечения качества в разработке ПО" в VK Образовании студенты изучают как такие системы как GitlabCI или Jenkins устроены изнутри.

Ссылка курса: https://park.vk.company/curriculum/program/discipline/1786/

P.S. По всем вопросам, пишите – @nikitarub. Issue приветсвуются :-)
```

## Как запустить

*Если вдруг забыли какие есть флаги:* `python3 src/main.py --help`

**Для начала нужны библиотеки:**
```
pip3 install -r requirements.txt
```

Попробуем запустить систему в explain режиме используя CLI. [подробнее про explain](#explain-режим). 

Будем запускать наш заготовленный проект [**target**](https://github.com/nikitarub/automation_qa_target).

```
python3 src/main.py target deploy backend -m cli --explain
```

В примере выше запускается выкатка бекенда для проекта target в режиме explain.

### Explain режим

Режим работы системы автоматиазции в которой будут показаны все вызываемые функции во время запуска модуля.

Аналогия – EXPLAIN в SQL запросах – когда будет показано, что будет сделано, но не применено к данным. 

Пример:

```
$ python3 src/main.py target deploy backend -m cli --explain 

[   INFO][ /automation_qa/src/common/explain.py:16    ]: Setting explain mode to True
[   INFO][ /automation_qa/src/main.py:44              ]: starting cli
[  DEBUG][ /automation_qa/src/modules/base.py:23      ]: Running `backend` function
[   INFO][ /automation_qa/src/modules/deploy.py:23    ]: Rolling out backend
[EXPLAIN][ /automation_qa/src/common/fs.py:30         ]: Asking for current path
[   INFO][ /automation_qa/src/modules/deploy.py:25    ]: Path is: /automation_qa
[   INFO][ /automation_qa/src/modules/deploy.py:26    ]: Updating version to patch
[   INFO][ /automation_qa/src/common/versioning.py:25 ]: Updating version: patch
[EXPLAIN][ /automation_qa/src/common/versioning.py:29 ]: Will read version file | with args: ('version.json', 'version')
[   INFO][ /automation_qa/src/common/versioning.py:36 ]: Version patched: 0.0.1
[   INFO][ /automation_qa/src/common/versioning.py:52 ]: Updating to version in file...
[EXPLAIN][ /automation_qa/src/common/versioning.py:54 ]: Version file will be updated | with args: ('version.json', {'version': '0.0.1'})
[   INFO][ /automation_qa/src/common/versioning.py:55 ]: Versioning file has been updated.
```

## Запуск системы в Webhook режиме (+ explain). 

CI содержит в себе HTTP API для работы как Webhook – слушать запросы для запуска необходимых процессов автоматизации.

```
$ python3 src/main.py -m webhook --explain

[   INFO][ /automation_qa/src/common/explain.py:16 ]: Setting explain mode to True
[   INFO][ /automation_qa/src/main.py:47           ]: starting webhook
INFO:     Started server process [53327]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:3000 (Press CTRL+C to quit)
```

Локально запускается [fastAPI](https://fastapi.tiangolo.com/) сервер на 3000 порту. 

В API уже заготовлен пример webhook для github. 

OpenAPI документация будет доступна по адресу: 

[http://127.0.0.1:3000](http://127.0.0.1:3000)

Триггернуть API можно простым curl:
```
curl -X 'POST' \
  'http://localhost:3000/github/' \
  -H 'accept: application/json' \
  -d ''
```
И в логах сервера будет: 

```
[   INFO][ /automation_qa/src/handlers/github_webhook/routers/github.py:24 ]: Got github webhook POST request
[   INFO][ /automation_qa/src/handlers/github_webhook/routers/github.py:26 ]: Done with github webhook POST request
[  DEBUG][ /automation_qa/src/modules/base.py:23      ]: Running `release_backend` function
[   INFO][ /automation_qa/src/scenario/scenario.py:24 ]: Starting release backend scenario
[EXPLAIN][ /automation_qa/src/common/fs.py:30         ]: Asking for current path
[   INFO][ /automation_qa/src/scenario/scenario.py:26 ]: Path is: /automation_qa
[   INFO][ /automation_qa/src/scenario/scenario.py:28 ]: Step 1: Repository
[  DEBUG][ /automation_qa/src/modules/base.py:23      ]: Running `clone` function
[   INFO][ /automation_qa/src/modules/github.py:25    ]: Cloning repository of git@github.com:nikitarub/automation_qa_target.git to ./target_test_project
[EXPLAIN][ /automation_qa/src/common/fs.py:35         ]: Checking if {path} exists | with args: ('./target_test_project',)
[   INFO][ /automation_qa/src/common/git.py:11        ]: Clonning git@github.com:nikitarub/automation_qa_target.git to path: ./target_test_project
[EXPLAIN][ /automation_qa/src/common/git.py:12        ]: cmd | with args: ('git clone git@github.com:nikitarub/automation_qa_target.git ./target_test_project',)
[   INFO][ /automation_qa/src/scenario/scenario.py:31 ]: Step 2: Working dir
[   INFO][ /automation_qa/src/common/fs.py:14         ]: Changing path to: ./target_test_project
[EXPLAIN][ /automation_qa/src/common/fs.py:15         ]: isdir | with args: ('./target_test_project',)
[EXPLAIN][ /automation_qa/src/common/fs.py:19         ]: chdir | with args: ('./target_test_project',)
[   INFO][ /automation_qa/src/scenario/scenario.py:34 ]: Step 3: Branch
[  DEBUG][ /automation_qa/src/modules/base.py:23      ]: Running `checkout` function
[   INFO][ /automation_qa/src/modules/github.py:37    ]: Checking out branch `master`
[   INFO][ /automation_qa/src/common/git.py:17        ]: Checkout master
[EXPLAIN][ /automation_qa/src/common/git.py:18        ]: cmd | with args: ('git checkout master',)
[   INFO][ /automation_qa/src/scenario/scenario.py:37 ]: Step 4: Branch
[  DEBUG][ /automation_qa/src/modules/base.py:23      ]: Running `pull` function
[   INFO][ /automation_qa/src/modules/github.py:43    ]: Pulling repo
[   INFO][ /automation_qa/src/common/git.py:23        ]: Pulling git repository
[EXPLAIN][ /automation_qa/src/common/git.py:24        ]: cmd | with args: ('git pull',)
[   INFO][ /automation_qa/src/scenario/scenario.py:40 ]: Step 5: Tests
[  DEBUG][ /automation_qa/src/modules/base.py:23      ]: Running `unit` function
[EXPLAIN][ /automation_qa/src/common/fs.py:30         ]: Asking for current path
[   INFO][ /automation_qa/src/modules/test.py:22      ]: Path is: /automation_qa
[   INFO][ /automation_qa/src/modules/test.py:26      ]: Running unit tests
[   INFO][ /automation_qa/src/scenario/scenario.py:43 ]: Step 6: Deploy
[  DEBUG][ /automation_qa/src/modules/base.py:23      ]: Running `backend` function
[   INFO][ /automation_qa/src/modules/deploy.py:23    ]: Rolling out backend
[EXPLAIN][ /automation_qa/src/common/fs.py:30         ]: Asking for current path
[   INFO][ /automation_qa/src/modules/deploy.py:25    ]: Path is: /automation_qa
[   INFO][ /automation_qa/src/modules/deploy.py:26    ]: Updating version to patch
[   INFO][ /automation_qa/src/common/versioning.py:25 ]: Updating version: patch
[EXPLAIN][ /automation_qa/src/common/versioning.py:29 ]: Will read version file | with args: ('version.json', 'version')
[   INFO][ /automation_qa/src/common/versioning.py:36 ]: Version patched: 0.0.1
[   INFO][ /automation_qa/src/common/versioning.py:52 ]: Updating to version in file...
[EXPLAIN][ /automation_qa/src/common/versioning.py:54 ]: Version file will be updated | with args: ('version.json', {'version': '0.0.1'})
[   INFO][ /automation_qa/src/common/versioning.py:55 ]: Versioning file has been updated.
[   INFO][ /automation_qa/src/scenario/scenario.py:46 ]: Step 7: Teardown
[   INFO][ /automation_qa/src/common/fs.py:14         ]: Changing path to: /automation_qa
[EXPLAIN][ /automation_qa/src/common/fs.py:15         ]: isdir | with args: ('/automation_qa',)
[EXPLAIN][ /automation_qa/src/common/fs.py:19         ]: chdir | with args: ('/automation_qa',)
INFO:     127.0.0.1:65067 - "POST /github/ HTTP/1.1" 200 OK
[   INFO][ /automation_qa/src/handlers/github_webhook/routers/github.py:19 ]: Sent telegram: Done processing all
```

## Архитектура

Файловая структура проекта, да и структура всех компонентов вдохновлена [Atomic-design](https://atomicdesign.bradfrost.com/):
* common – общие файлы, в них лежит реализация функций, которые выполняют какую-то конечную работу.
* modules – модули содержат в себе последовательности классы, которые реализуют какую-то логику, например Github.pull()
* scenario – сценарии, это собранные шаги состоящии из вызовов методов из модулей.
* configs – конфигурации проектов единообразно организованные в виде классов.
* handlers – обработчики, которые поддерживает система автоматизации. CLI и Webhook.
