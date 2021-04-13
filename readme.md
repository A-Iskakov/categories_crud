#  CRUD todo's, categories
TODO webapp:
- CRUD todo's, categories (can be nested)
- Only REST api
- Caching, env settings
- Project requirements, README file (setup, deploy instructions, version status etc.)
- Use docker, docker-compose
- Write unit tests
- Ready to production
- Encrypt some todo's with symmetric encryption (optional)

To launch application do the following

`git clone git@github.com:A-Iskakov/categories_crud.git`

`cd categories_crud`

`cp example.env .env`

`docker-compose up --detach --build`

you may also run tests explicitly

`docker exec -it categories_crud_web_1 python manage.py test backend.tests`

Then you can open this page to see API root schema
`localhost:8080/api/schema/swagger-ui/`