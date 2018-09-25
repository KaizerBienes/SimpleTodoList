# SimpleTodoList

This is a simple todo list that was implemented with Flask and Vue.js.

### Project Milestones

#### Basic requirements
- [x] I should be able to save and view to-dos.
- [x] I should be able to order my to-dos by date
- [x] I should be able to delete to-dos
- [x] I should be able to add tags for every to-do (Bonus x1)
- [x] I should be able to see top 3 most used tags when creating a to-do(Bonus x2)

#### Consider the following data entities in your database:
- [x] Tasks (List of all to-dos)
- [x] Tags (Bonus x1)
#### Bonus
- [x] Create your service as RESTful API (Bonus x1)
- [ ] Insert your application into a docker container/s with a corresponding docker file or shell script (Bonus x2)
- [x] Create database migration scripts (Bonus x1)
- [ ] Add Unit-Testing (Bonus x2)
- [x] User Log-in (Bonus x2)

### Cloning the repository
Cloning this repository with the given statement:
```bash
git clone https://github.com/KaizerBienes/SimpleTodoList.git
```

### Back-end setup

#### Setting up the backend dependencies
Dependencies should be installed through requirements.txt which contains all of the install dependencies.
```bash
cd SimpleTodoList/backend/
sudo apt-get install python-pip
pip install virtual env
virtualenv backend
source backend/bin/activate
pip install -r requirements.txt
```

#### Setting up the database through the migration script
I primarily used SQLite for this one.
```bash
flask db upgrade
```

#### Actual running of the script
```bash
source setup/env-var.py
flask run
```

### Front-end setup

#### Installing Frontend
```bash
cd SimpleTodoList/frontend/
npm install
```

#### Running in Dev
```bash
npm run dev
```
Both servers must be run on separate instances because they are hosted differently: one for Flask and another for Vue. Until we deploy this to a live hosting, we can just stick to the dev-ready setup.
