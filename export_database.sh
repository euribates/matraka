#!/usr/bin/env bash

./manage.py dumpdata tags --indent 4 --natural-foreign > fixtures/tags.json
./manage.py dumpdata questions --indent 4 --natural-foreign > fixtures/questions.json
